from rest_framework import viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework.versioning import URLPathVersioning
from rest_framework.throttling import UserRateThrottle
from rest_framework.schemas.openapi import AutoSchema
from rest_framework import renderers
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from datetime import timedelta
import asyncio
import logging
from asgiref.sync import async_to_sync

from .models import StudentExtra, Book, IssuedBook
from .serializers import StudentExtraSerializer, BookSerializer, IssuedBookSerializer

logger = logging.getLogger(__name__)

class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 4

class CustomThrottle(UserRateThrottle):
    rate = '502/day'

class IsLibrarianOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.groups.filter(name='Librarians').exists())

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLibrarianOrAdmin]
    pagination_class = CustomPagination
    versioning_class = URLPathVersioning
    throttle_classes = [CustomThrottle]
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    async def perform_async_task(self, task_id):
        await asyncio.sleep(1)
        logger.info(f"Выполнена асинхронная задача {task_id}")

    def async_operation(self):
        async_to_sync(self._run_async_tasks)()

    async def _run_async_tasks(self):
        async_tasks = [self.perform_async_task(i) for i in range(5)]
        await asyncio.gather(*async_tasks)

class StudentExtraViewSet(BaseViewSet):
    queryset = StudentExtra.objects.all()
    serializer_class = StudentExtraSerializer
    search_fields = ['id']
    schema = AutoSchema(tags=['StudentExtra'], operation_id_base='studentextra')

    @action(detail=False, methods=['get'], url_path='count')
    def count_students(self, request):
        count = cache.get_or_set("student_count", self.get_queryset().count(), timeout=300)
        return Response({"count": count})

class BookViewSet(BaseViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ["id", "name", "isbn", "author", "category"]
    ordering_fields = ["id", "name", "author"]
    ordering = ["id"]
    schema = AutoSchema(tags=['Book'], operation_id_base='book')

    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return Response({"error": "Неверный формат данных"}, status=status.HTTP_400_BAD_REQUEST)
        deleted_count, _ = self.queryset.filter(id__in=ids).delete()
        return Response({"deleted": deleted_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='by-author')
    def books_by_author(self, request):
        author = request.query_params.get("author")
        if not author:
            return Response({"error": "Не указан автор"}, status=status.HTTP_400_BAD_REQUEST)
        books = cache.get_or_set(f"books_by_{author}", list(self.get_queryset().filter(author__icontains=author)), timeout=300)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class IssuedBookViewSet(BaseViewSet):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer
    search_fields = ["id", "enrollment", "isbn", "issuedate", "expirydate"]
    schema = AutoSchema(tags=['IssuedBook'], operation_id_base='issuedbook')

    @action(detail=True, methods=['post'], url_path='issue')
    def issue_book(self, request, pk=None):
        issued_book = self.get_object()
        if issued_book.expirydate:
            return Response({"error": "Книга уже выдана!"}, status=status.HTTP_400_BAD_REQUEST)
        issued_book.issuedate = timezone.now()
        issued_book.expirydate = timezone.now() + timedelta(days=30)
        issued_book.save()
        logger.info(f"Книга {issued_book.id} выдана")
        return Response({"message": "Книга выдана!"}, status=status.HTTP_200_OK)
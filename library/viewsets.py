from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.versioning import URLPathVersioning
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas.openapi import AutoSchema
from .models import StudentExtra, Book, IssuedBook
from .serializers import StudentExtraSerializer, BookSerializer, IssuedBookSerializer
import asyncio
from rest_framework import renderers
from rest_framework.settings import api_settings

class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 4

class CustomThrottle(UserRateThrottle):
    rate = '502/day'  # ограничение на 52 запроса в день

class StudentExtraViewSet(viewsets.ModelViewSet):
    queryset = StudentExtra.objects.all()
    serializer_class = StudentExtraSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Добавляем пагинацию
    permission_classes = [IsAdminUser]#auth
    versioning_class = URLPathVersioning#vers
    throttle_classes = [UserRateThrottle]#дросель
    throttle_scope = getattr(api_settings, 'DEFAULT_THROTTLE_RATES', None)
    pagination_class.default_pate_size = getattr(api_settings, 'PAGE_SIZE', 10)
    schema = AutoSchema(tags=['StudentExtra'], operation_id_base='studentextra')
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]  # Указываем поддерживаемые форматы (JSON и Browsable API)
    async def perform_async_task(self, task_id):
        # Асинхронная операция, которая может быть выполнена в фоновом режиме
        await asyncio.sleep(1)
        print(f"Выполнено асинхронной задачи {task_id}")

    def async_operation(self):
        # Создание сопрограммы для выполнения асинхронной задачи
        async_tasks = [self.perform_async_task(i) for i in range(5)]

        # Запуск всех сопрограмм
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*async_tasks))
        loop.close()

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["id","name","isbn","author","category"]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Добавляем пагинацию
    permission_classes = [IsAdminUser]#auth
    versioning_class = URLPathVersioning#vers
    throttle_classes = [UserRateThrottle]#дросель
    throttle_scope = getattr(api_settings, 'DEFAULT_THROTTLE_RATES', None)
    pagination_class.default_pate_size = getattr(api_settings, 'PAGE_SIZE', 10)
    schema = AutoSchema(tags=['Book'], operation_id_base='book')
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]  # Указываем поддерживаемые форматы (JSON и Browsable API)
    async def perform_async_task(self, task_id):
        # Асинхронная операция, которая может быть выполнена в фоновом режиме
        await asyncio.sleep(1)
        print(f"Выполнено асинхронной задачи {task_id}")

    def async_operation(self):
        # Создание сопрограммы для выполнения асинхронной задачи
        async_tasks = [self.perform_async_task(i) for i in range(5)]

        # Запуск всех сопрограмм
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*async_tasks))
        loop.close()
  

class IssuedBookViewSet(viewsets.ModelViewSet):
    queryset = IssuedBook.objects.all()
    serializer_class = IssuedBookSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    search_fields = ["id","enrollment","isbn","issuedate","expirydate"]
    pagination_class = CustomPagination  # Добавляем пагинацию
    permission_classes = [IsAdminUser] #auth
    versioning_class = URLPathVersioning#vers
    throttle_classes = [UserRateThrottle]#дросель
    throttle_scope = getattr(api_settings, 'DEFAULT_THROTTLE_RATES', None)
    pagination_class.default_pate_size = getattr(api_settings, 'PAGE_SIZE', 10)
    schema = AutoSchema(tags=['IssuedBook'], operation_id_base='issuedbook')
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]  # Указываем поддерживаемые форматы (JSON и Browsable API)
    async def perform_async_task(self, task_id):
        # Асинхронная операция, которая может быть выполнена в фоновом режиме
        await asyncio.sleep(1)
        print(f"Выполнено асинхронной задачи {task_id}")

    def async_operation(self):
        # Создание сопрограммы для выполнения асинхронной задачи
        async_tasks = [self.perform_async_task(i) for i in range(5)]

        # Запуск всех сопрограмм
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*async_tasks))
        loop.close()




from rest_framework import serializers, viewsets
from .models import StudentExtra, Book, IssuedBook

class StudentExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExtra
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.IntegerField()

    class Meta:
        model = Book
        fields = '__all__'

class IssuedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedBook
        fields = '__all__'

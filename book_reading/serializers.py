from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookWithoutFullDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['full_description']


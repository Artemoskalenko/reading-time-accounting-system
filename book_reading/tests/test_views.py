import datetime

import pytest

from unittest import mock

from rest_framework.test import APIClient

from book_reading.models import Book, ReadingStatistics, ReadingSession, UserStatistics
from book_reading.serializers import BookWithoutFullDescriptionSerializer
from book_reading.services import timedelta_to_string
from book_reading.tasks import daily_collection_of_user_statistics


@pytest.mark.django_db
def test_book_api():
    client = APIClient()

    book = Book.objects.create(
        title='test_title',
        author='test_author',
        year_published=2023,
        short_description='test_short_description',
        full_description='test_full_description',
    )

    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert len(response.data) == 1

    book_id = response.data[0]["id"]

    response = client.get(f"/api/v1/book-details/{book_id}/")
    assert response.status_code == 200
    assert response.data["title"] == book.title


@pytest.mark.django_db
def test_reading_statistics_api():
    client = APIClient()

    client.post("/auth/users/", {"username": "testusername", "password": "testpassword"})
    response = client.post("/auth/token/login/", {"username": "testusername", "password": "testpassword"})
    client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['auth_token']}")

    book = Book.objects.create(
        title='test_title',
        author='test_author',
        year_published=2023,
        short_description='test_short_description',
        full_description='test_full_description',
    )
    book2 = Book.objects.create(
        title='test_title2',
        author='test_author2',
        year_published=2022,
        short_description='test_short_description2',
        full_description='test_full_description2',
    )
    book_serialized = BookWithoutFullDescriptionSerializer(book)

    response = client.get(f"/api/v1/book-reading-statistics/{book.id - 1}/")
    assert response.status_code == 200
    assert response.data["Error"] == "There is no book with this ID"

    response = client.get(f"/api/v1/book-reading-statistics/{book.id}/")
    assert response.status_code == 200
    assert response.data["Book"] == book_serialized.data
    assert response.data["Total reading time"] == timedelta_to_string(datetime.timedelta())

    response = client.get(f"/api/v1/start-reading-session/{book.id - 1}/")
    assert response.status_code == 200
    assert response.data["Error"] == "There is no book with this ID"

    response = client.get(f"/api/v1/start-reading-session/{book.id}/")
    assert response.status_code == 200
    assert response.data["message"] == "Book reading session started successfully"

    response = client.get(f"/api/v1/start-reading-session/{book.id}/")
    assert response.status_code == 200
    assert response.data["message"] == "A reading session for this book is already active"

    response = client.get(f"/api/v1/start-reading-session/{book2.id}/")
    assert response.status_code == 200
    assert response.data["message"] == 'The previous book reading session was ended successfully, ' \
                                       'and the new book reading session started successfully'

    response = client.get(f"/api/v1/end-reading-session/")
    assert response.status_code == 200
    assert response.data["message"] == "Book reading session ended successfully"

    response = client.get(f"/api/v1/end-reading-session/")
    assert response.status_code == 200
    assert response.data["message"] == "There is currently no book reading session started"

    mocked = datetime.datetime.now() - datetime.timedelta(hours=2)
    with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
        client.get(f"/api/v1/start-reading-session/{book.id}/")
    client.get(f"/api/v1/end-reading-session/")
    response = client.get(f"/api/v1/book-reading-statistics/{book.id}/")
    assert response.status_code == 200
    assert response.data["Book"] == book_serialized.data
    assert response.data["Total reading time"] == timedelta_to_string(datetime.timedelta(hours=2))

    daily_collection_of_user_statistics()
    response = client.get(f"/api/v1/user-statistics/")
    assert response.status_code == 200
    assert response.data["Total reading time"] == timedelta_to_string(datetime.timedelta(hours=2))
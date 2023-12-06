import datetime

import pytest

from unittest import mock

from rest_framework.test import APIClient

from book_reading.models import Book
from book_reading.serializers import BookWithoutFullDescriptionSerializer
from book_reading.services import timedelta_to_string
from book_reading.tasks import daily_collection_of_user_statistics


@pytest.fixture
def create_book_1():
    """Creates the first book"""
    book_data = {'title': 'test_title',
                 'author': 'test_author',
                 'year_published': 2023,
                 'short_description': 'test_short_description',
                 'full_description': 'test_full_description'}
    book = Book.objects.create(**book_data)
    return book


@pytest.fixture
def create_book_2():
    """Creates the second book"""
    book_data = {'title': 'test_title2',
                 'author': 'test_author2',
                 'year_published': 2022,
                 'short_description': 'test_short_description2',
                 'full_description': 'test_full_description2'}
    book = Book.objects.create(**book_data)
    return book


@pytest.fixture
def api_client():
    """Returns the APIClient for making requests"""
    return APIClient()


@pytest.fixture
def test_user(api_client):
    """Creates a user by token"""
    response = api_client.post("/auth/users/", {"username": "testusername", "password": "testpassword"})
    user_id = response.data["id"]
    response = api_client.post("/auth/token/login/", {"username": "testusername", "password": "testpassword"})
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['auth_token']}")
    return user_id


@pytest.fixture
def start_reading_session(api_client, create_book_1):
    """Begins the process of reading a book"""
    api_client.get(f"/api/v1/start-reading-session/{create_book_1.id}/")


@pytest.fixture
def reading_a_book_for_two_hours(api_client, create_book_1, test_user):
    """Simulate reading a book for two hours"""
    mocked = datetime.datetime.now() - datetime.timedelta(hours=2)
    with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
        api_client.get(f"/api/v1/start-reading-session/{create_book_1.id}/")
    api_client.get(f"/api/v1/end-reading-session/")


@pytest.mark.django_db
class TestBooks:
    def test_books_url(self, api_client, create_book_1):
        response = api_client.get("/api/v1/books/")
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_book_details_url(self, api_client, create_book_1):
        response = api_client.get(f"/api/v1/book-details/{create_book_1.id}/")
        assert response.status_code == 200
        assert response.data["title"] == 'test_title'
        assert response.data["author"] == 'test_author'
        assert response.data["year_published"] == 2023
        assert response.data["short_description"] == 'test_short_description'
        assert response.data["full_description"] == 'test_full_description'


@pytest.mark.django_db
class TestBookReadingStatistics:
    def test_book_reading_statistics_invalid_book_id(self, create_book_1, create_book_2, api_client, test_user):
        response = api_client.get(f"/api/v1/book-reading-statistics/{create_book_2.id + 1}/")
        assert response.status_code == 200
        assert response.data["Error"] == "There is no book with this ID"

    def test_book_reading_statistics_with_zero_total_reading_time(self, create_book_1, create_book_2, api_client, test_user):
        book_serialized = BookWithoutFullDescriptionSerializer(create_book_1)

        response = api_client.get(f"/api/v1/book-reading-statistics/{create_book_1.id}/")
        assert response.status_code == 200
        assert response.data["Book"] == book_serialized.data
        assert response.data["Total reading time"] == timedelta_to_string(datetime.timedelta())


@pytest.mark.django_db
class TestBookReadingSession:
    def test_start_reading_session_invalid_book_id(self, create_book_1, create_book_2, api_client, test_user):
        response = api_client.get(f"/api/v1/start-reading-session/{create_book_2.id + 1}/")
        assert response.status_code == 200
        assert response.data["Error"] == "There is no book with this ID"

    def test_start_reading_session(self, create_book_1, create_book_2, api_client, test_user):
        response = api_client.get(f"/api/v1/start-reading-session/{create_book_1.id}/")
        assert response.status_code == 200
        assert response.data["message"] == "Book reading session started successfully"

    def test_start_reading_session_already_active(self, create_book_1, create_book_2,
                                                  api_client, test_user, start_reading_session):
        response = api_client.get(f"/api/v1/start-reading-session/{create_book_1.id}/")
        assert response.status_code == 200
        assert response.data["message"] == "A reading session for this book is already active"

    def test_start_reading_session_with_active_session(self, create_book_1, create_book_2,
                                                       api_client, test_user, start_reading_session):
        response = api_client.get(f"/api/v1/start-reading-session/{create_book_2.id}/")
        assert response.status_code == 200
        assert response.data["message"] == 'The previous book reading session was ended successfully, ' \
                                           'and the new book reading session started successfully'

    def test_end_reading_session_with_active_session(self, create_book_1, create_book_2,
                                                     api_client, test_user, start_reading_session):
        response = api_client.get(f"/api/v1/end-reading-session/")
        assert response.status_code == 200
        assert response.data["message"] == "Book reading session ended successfully"

    def test_end_reading_session_without_active_session(self, create_book_1, create_book_2,
                                                        api_client, test_user):
        response = api_client.get(f"/api/v1/end-reading-session/")
        assert response.status_code == 200
        assert response.data["message"] == "There is currently no book reading session started"


@pytest.mark.django_db
class TestUserReadingStatistics:
    def test_user_reading_statistics_with_zero_total_reading_time(self, api_client, create_book_1, test_user):
        """Testing general user statistics without reading the book before"""
        daily_collection_of_user_statistics()

        response = api_client.get(f"/api/v1/user-statistics/")
        assert response.status_code == 200
        assert response.data["Total reading time"] == timedelta_to_string(datetime.timedelta())
        assert response.data["Last 7 days reading time"] == timedelta_to_string(datetime.timedelta())
        assert response.data["Last 30 days reading time"] == timedelta_to_string(datetime.timedelta())

    def test_user_reading_statistics(self, api_client, create_book_1, test_user, reading_a_book_for_two_hours):
        """Testing general user statistics after two hours of reading a book"""
        daily_collection_of_user_statistics()

        response = api_client.get(f"/api/v1/user-statistics/")
        assert response.status_code == 200
        assert response.data["Total reading time"] == timedelta_to_string(datetime.timedelta(hours=2))
        assert response.data["Last 7 days reading time"] == timedelta_to_string(datetime.timedelta(hours=2))
        assert response.data["Last 30 days reading time"] == timedelta_to_string(datetime.timedelta(hours=2))

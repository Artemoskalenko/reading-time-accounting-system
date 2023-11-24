import datetime

import pytest
import pytz

from django.contrib.auth.models import User
from unittest import mock

from book_reading.models import Book, ReadingStatistics, ReadingSession, UserStatistics


@pytest.mark.django_db
def test_book_model():
    book = Book.objects.create(
        title='test_title',
        author='test_author',
        year_published=2023,
        short_description='test_short_description',
        full_description='test_full_description',
    )
    assert book.id is not None
    assert book.title == 'test_title'
    assert book.author == 'test_author'
    assert book.year_published == 2023
    assert book.short_description == 'test_short_description'
    assert book.full_description == 'test_full_description'


@pytest.mark.django_db
def test_reading_session_model():
    mocked = datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('Europe/Kiev'))
    book = Book.objects.create(
        title='test_title',
        author='test_author',
        year_published=2023,
        short_description='test_short_description',
        full_description='test_full_description',
    )
    user = User.objects.create_user(username='testusername',
                                    password='testpassword')
    with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
        reading_session = ReadingSession.objects.create(book=book, user=user)

    assert reading_session.id is not None
    assert reading_session.book.title == 'test_title'
    assert reading_session.user.username == 'testusername'
    assert reading_session.start_time.strftime('%Y-%m-%d %H:%M') == '2023-01-01 00:00'


@pytest.mark.django_db
def test_reading_statistics_model():
    book = Book.objects.create(
        title='test_title',
        author='test_author',
        year_published=2023,
        short_description='test_short_description',
        full_description='test_full_description',
    )
    user = User.objects.create_user(username='testusername',
                                    password='testpassword')
    reading_statistics = ReadingStatistics.objects.create(book=book, user=user)

    assert reading_statistics.id is not None
    assert reading_statistics.book.title == 'test_title'
    assert reading_statistics.user.username == 'testusername'
    assert reading_statistics.total_reading_time == datetime.timedelta()


@pytest.mark.django_db
def test_user_statistics_model():
    user = User.objects.create_user(username='testusername',
                                    password='testpassword')
    user_statistics = UserStatistics.objects.create(user=user)

    assert user_statistics.id is not None
    assert user_statistics.user.username == 'testusername'
    assert user_statistics.total_reading_time == datetime.timedelta()
    assert user_statistics.last_7_days_reading_time == datetime.timedelta()
    assert user_statistics.last_30_days_reading_time == datetime.timedelta()


import datetime

import pytest

from book_reading.services import timedelta_to_string, collect_user_reading_statistics,\
    start_reading_session_and_get_message, end_reading_session_and_get_message,\
    get_user_statistics, get_user_reading_statistics

from .test_views import api_client, create_book_1, create_book_2, test_user,\
    reading_a_book_for_two_hours, start_reading_session
from ..serializers import BookWithoutFullDescriptionSerializer
from ..tasks import daily_collection_of_user_statistics


class TestTimedeltaToString:
    def test_timedelta_to_string_seconds(self):
        time = datetime.timedelta(seconds=20)
        assert timedelta_to_string(time) == "0 min 20 sec"

    def test_timedelta_to_string_minutes(self):
        time = datetime.timedelta(minutes=20, seconds=20)
        assert timedelta_to_string(time) == "20 min 20 sec"

    def test_timedelta_to_string_hours(self):
        time = datetime.timedelta(hours=20, minutes=20, seconds=20)
        assert timedelta_to_string(time) == "20 hours, 20 min 20 sec"

    def test_timedelta_to_string_zero_time(self):
        time = datetime.timedelta()
        assert timedelta_to_string(time) == "0 min 0 sec"


@pytest.mark.django_db
class TestCollectUserReadingStatistics:
    def test_collect_user_reading_statistics_with_zero_total_reading_time(self, api_client, create_book_1, test_user):
        result = collect_user_reading_statistics(user_id=test_user, days=7)
        assert result == datetime.timedelta()

    def test_collect_user_reading_statistics(self, api_client, create_book_1, test_user, reading_a_book_for_two_hours):
        result = collect_user_reading_statistics(user_id=test_user, days=7)
        assert timedelta_to_string(result) == timedelta_to_string(datetime.timedelta(hours=2))

    def test_collect_user_reading_statistics_for_zero_days(self, api_client, create_book_1, test_user, reading_a_book_for_two_hours):
        result = collect_user_reading_statistics(user_id=test_user, days=0)
        assert result == datetime.timedelta()


@pytest.mark.django_db
class TestStartReadingSessionAndGetMessage:
    def test_start_reading_session_and_get_message_invalid_book_id(self, create_book_1, create_book_2,
                                                                   api_client, test_user):
        result = start_reading_session_and_get_message(user=test_user, book_id=(create_book_2.id + 1))
        assert result.get("Error") == "There is no book with this ID"

    def test_start_reading_session_and_get_message(self, create_book_1, create_book_2, api_client, test_user):
        result = start_reading_session_and_get_message(user=test_user, book_id=create_book_1.id)
        assert result.get("message") == "Book reading session started successfully"

    def test_start_reading_session_and_get_message_already_active(self, create_book_1, create_book_2,
                                                                  api_client, test_user, start_reading_session):
        result = start_reading_session_and_get_message(user=test_user, book_id=create_book_1.id)
        assert result.get("message") == "A reading session for this book is already active"

    def test_start_reading_session_and_get_message_with_active_session(self, create_book_1, create_book_2,
                                                                       api_client, test_user, start_reading_session):
        result = start_reading_session_and_get_message(user=test_user, book_id=create_book_2.id)
        assert result.get("message") == 'The previous book reading session was ended successfully, ' \
                                        'and the new book reading session started successfully'


@pytest.mark.django_db
class TestEndReadingSessionAndGetMessage:
    def test_end_reading_session_and_get_message_with_active_session(self, create_book_1, create_book_2,
                                                                     api_client, test_user, start_reading_session):
        result = end_reading_session_and_get_message(user=test_user)
        assert result.get("message") == "Book reading session ended successfully"

    def test_end_reading_session_and_get_message_without_active_session(self, create_book_1, create_book_2,
                                                                        api_client, test_user):
        result = end_reading_session_and_get_message(user=test_user)
        assert result.get("message") == "There is currently no book reading session started"


@pytest.mark.django_db
class TestGetUserStatistics:
    def test_get_user_statistics_with_zero_total_reading_time(self, api_client, create_book_1, test_user):
        result = get_user_statistics(user=test_user)
        assert timedelta_to_string(result.get("total_reading_time")) == timedelta_to_string(datetime.timedelta())
        assert timedelta_to_string(result.get("last_7_days_reading_time")) == timedelta_to_string(datetime.timedelta())
        assert timedelta_to_string(result.get("last_30_days_reading_time")) == timedelta_to_string(datetime.timedelta())

    def test_get_user_statistics(self, api_client, create_book_1, test_user, reading_a_book_for_two_hours):
        result = get_user_statistics(user=test_user)
        assert timedelta_to_string(result.get("total_reading_time")) == timedelta_to_string(datetime.timedelta(hours=2))
        assert timedelta_to_string(result.get("last_7_days_reading_time")) == timedelta_to_string(datetime.timedelta())
        assert timedelta_to_string(result.get("last_30_days_reading_time")) == timedelta_to_string(datetime.timedelta())

    def test_get_user_statistics_with_celery_task(self, api_client, create_book_1, test_user, reading_a_book_for_two_hours):
        daily_collection_of_user_statistics()
        result = get_user_statistics(user=test_user)
        assert timedelta_to_string(result.get("total_reading_time")) == timedelta_to_string(datetime.timedelta(hours=2))
        assert timedelta_to_string(result.get("last_7_days_reading_time")) == timedelta_to_string(datetime.timedelta(hours=2))
        assert timedelta_to_string(result.get("last_30_days_reading_time")) == timedelta_to_string(datetime.timedelta(hours=2))


@pytest.mark.django_db
class TestGetUserReadingStatistics:
    def test_book_reading_statistics_invalid_book_id(self, create_book_1, create_book_2, api_client, test_user):
        result = get_user_reading_statistics(user=test_user, book_id=(create_book_2.id + 1))
        assert result.get("Error") == "There is no book with this ID"

    def test_book_reading_statistics_with_zero_total_reading_time(self, create_book_1, create_book_2, api_client,
                                                                  test_user):
        book_serialized = BookWithoutFullDescriptionSerializer(create_book_1)

        result = get_user_reading_statistics(user=test_user, book_id=create_book_1.id)
        assert result.get("Book") == book_serialized.data
        assert result.get("Total reading time") == timedelta_to_string(datetime.timedelta())


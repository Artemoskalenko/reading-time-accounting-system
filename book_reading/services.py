import datetime
import pytz
from django.contrib.auth.models import User

from django.db.models import Sum

from .models import ReadingSession, ReadingStatistics, UserStatistics, Book
from .serializers import BookWithoutFullDescriptionSerializer

KIEV_TZ = pytz.timezone('Europe/Kiev')


def _get_user(user):
    if type(user) == int:
        user = User.objects.get(id=user)
    return user


def _end_active_reading_session(user) -> None:
    """
    The function ends the book reading session,
    updates book reading statistics and general user statistics.
    """
    active_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()
    book = active_session.book
    active_session.end_time = datetime.datetime.now(KIEV_TZ)
    active_session.duration = active_session.end_time - active_session.start_time
    active_session.save()

    _update_book_reading_statistics(user=user, book=book, duration=active_session.duration)
    _update_general_user_statistics(user=user, duration=active_session.duration)


def _update_general_user_statistics(user, duration) -> None:
    """Adds book reading time to the user's general statistics"""
    try:
        user_statistics = UserStatistics.objects.get(user=user)
    except UserStatistics.DoesNotExist:
        user_statistics = UserStatistics(user=user)
    user_statistics.total_reading_time += duration
    user_statistics.save()


def _update_book_reading_statistics(user, book, duration) -> None:
    """Adds the reading time to the user's statistics for a specific book"""
    try:
        reading_statistics = ReadingStatistics.objects.get(user=user, book=book)
    except ReadingStatistics.DoesNotExist:
        reading_statistics = ReadingStatistics(user=user, book=book)
    reading_statistics.total_reading_time += duration
    reading_statistics.save()


def timedelta_to_string(timedelta) -> str:
    """ A function to convert a datetime.timedelta object to a string."""
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours:
        result = f'{hours} hours, {minutes} min {seconds} sec'
    else:
        result = f'{minutes} min {seconds} sec'
    return result


def collect_user_reading_statistics(user_id: int, days: int):
    """
    Function for getting the total reading time of a user
    for a certain number of recent days
    """
    period_of_time = datetime.datetime.now(KIEV_TZ) - datetime.timedelta(days=days)

    total_duration = ReadingSession.objects.filter(
        user_id=user_id,
        start_time__gte=period_of_time
    ).aggregate(
        total_duration=Sum('duration')
    )['total_duration']
    if not total_duration:
        total_duration = datetime.timedelta()
    return total_duration


def start_reading_session_and_get_message(user, book_id):
    """
    Starts a new book reading session.
    Returns a dict with a message or with an error.
    """
    user = _get_user(user)

    active_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return {'Error': 'There is no book with this ID'}

    if active_session and active_session.book == book:
        response = {'message': 'A reading session for this book is already active'}
    elif active_session:
        _end_active_reading_session(user=user)
        ReadingSession.objects.create(book=book, user=user)
        response = {'message': 'The previous book reading session was ended successfully, '
                               'and the new book reading session started successfully'}
    elif not active_session:
        ReadingSession.objects.create(book=book, user=user)
        response = {'message': 'Book reading session started successfully'}

    return response


def end_reading_session_and_get_message(user):
    """
    Ends the current book reading session, if one exists.
    Returns a dict with a message or with an error.
    """
    user = _get_user(user)

    active_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()
    if active_session:
        _end_active_reading_session(user=user)
        response = {'message': 'Book reading session ended successfully'}
    else:
        response = {'message': 'There is currently no book reading session started'}
    return response


def get_user_statistics(user):
    """Returns common user statistics"""
    user = _get_user(user)
    try:
        user_statistics = user.statistics
    except UserStatistics.DoesNotExist:
        user_statistics = UserStatistics(user=user)
        user_statistics.save()
    return {"total_reading_time": user_statistics.total_reading_time,
            "last_7_days_reading_time": user_statistics.last_7_days_reading_time,
            "last_30_days_reading_time": user_statistics.last_30_days_reading_time}


def get_user_reading_statistics(user, book_id):
    """Returns user statistics for a specific book"""
    user = _get_user(user)
    try:
        book = Book.objects.get(id=book_id)
        book_serialized = BookWithoutFullDescriptionSerializer(book)

        # Checking whether user statistics exist for this book. If not, we create it.
        try:
            reading_statistics = ReadingStatistics.objects.get(user=user, book=book)
        except ReadingStatistics.DoesNotExist:
            reading_statistics = ReadingStatistics(user=user, book=book)
            reading_statistics.save()
        total_reading_time = reading_statistics.total_reading_time
        response = {'Book': book_serialized.data, 'Total reading time': timedelta_to_string(total_reading_time)}
    except Book.DoesNotExist:
        response = {'Error': 'There is no book with this ID'}

    return response

import datetime

from .models import ReadingSession, ReadingStatistics, UserStatistics


def end_book_reading_session(session_id: int):
    """
    The function ends the book reading session, updates book reading statistics and general user statistics.
    """
    active_session = ReadingSession.objects.get(id=session_id)
    user = active_session.user
    book = active_session.book
    active_session.end_time = datetime.datetime.now(datetime.timezone.utc)
    active_session.duration = active_session.end_time - active_session.start_time
    active_session.save()

    # Update book reading statistics
    try:
        reading_statistics = ReadingStatistics.objects.get(user=user, book=book)
    except ReadingStatistics.DoesNotExist:
        reading_statistics = ReadingStatistics(user=user, book=book)
    reading_statistics.total_reading_time += active_session.duration
    reading_statistics.save()

    # Update general user statistics.
    try:
        user_statistics = UserStatistics.objects.get(user=user)
    except UserStatistics.DoesNotExist:
        user_statistics = UserStatistics(user=user)
    user_statistics.total_reading_time += active_session.duration
    user_statistics.save()


def timedelta_to_string(timedelta):
    """
    A function to convert a datetime.timedelta object to a string.
    """
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    result = f'{hours} hours, {minutes} min {seconds} sec' if hours else f'{minutes} min {seconds} sec'
    return result


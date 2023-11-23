from celery import shared_task
from django.contrib.auth.models import User

from .models import UserStatistics
from .services import collect_user_reading_statistics


@shared_task
def daily_collection_of_user_statistics() -> None:
    """
    Task for daily collection of user reading statistics for the last 7 and 30 days
    """
    users = User.objects.all()

    for user in users:
        last_7_days_reading_time = collect_user_reading_statistics(user_id=user.id, days=7)
        last_30_days_reading_time = collect_user_reading_statistics(user_id=user.id, days=30)
        print(last_7_days_reading_time)
        print(last_30_days_reading_time)
        print(user.username)
        try:
            user_statistics = UserStatistics.objects.get(user=user)
        except UserStatistics.DoesNotExist:
            user_statistics = UserStatistics(user=user)

        user_statistics.last_7_days_reading_time = last_7_days_reading_time
        user_statistics.last_30_days_reading_time = last_30_days_reading_time
        print(user_statistics.last_7_days_reading_time)
        print(type(user_statistics.last_7_days_reading_time))
        user_statistics.save()




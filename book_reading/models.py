from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_published = models.IntegerField()
    short_description = models.TextField()
    full_description = models.TextField()


class ReadingSession(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(default=timedelta())


class ReadingStatistics(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_reading_time = models.DurationField(default=timedelta())


class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='statistics')
    total_reading_time = models.DurationField(default=timedelta())
    last_7_days_reading_time = models.DurationField(default=timedelta())
    last_30_days_reading_time = models.DurationField(default=timedelta())

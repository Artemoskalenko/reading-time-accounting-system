# Generated by Django 4.2.7 on 2023-12-04 14:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('year_published', models.IntegerField()),
                ('short_description', models.TextField()),
                ('full_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_reading_time', models.DurationField(default=datetime.timedelta(0))),
                ('last_7_days_reading_time', models.DurationField(default=datetime.timedelta(0))),
                ('last_30_days_reading_time', models.DurationField(default=datetime.timedelta(0))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_reading_time', models.DurationField(default=datetime.timedelta(0))),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_reading.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_reading.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
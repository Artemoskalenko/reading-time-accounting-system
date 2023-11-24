from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserStatistics, Book, ReadingStatistics


class UserStatisticsInline(admin.StackedInline):
    model = UserStatistics
    can_delete = False
    verbose_name_plural = "user_statistics"


class UserAdmin(BaseUserAdmin):
    inlines = [UserStatisticsInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Book)
admin.site.register(ReadingStatistics)

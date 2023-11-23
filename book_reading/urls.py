from django.urls import path

from . import views

urlpatterns = [
    path('books/', views.BookAPIList.as_view(), name='books'),
    path('book-details/<int:pk>/', views.BookAPIRetrieve.as_view(), name='book_details'),
    path('start-reading-session/<int:pk>/', views.ReadingSessionAPIView.as_view(), name='start_reading_session'),
    path('end-reading-session/', views.ReadingSessionAPIView.as_view(), name='end_reading_session'),
    path('user-statistics/', views.UserStatisticsAPIView.as_view(), name='user_statistics'),
    path('book-reading-statistics/<int:pk>/', views.ReadingStatisticsAPIView.as_view(), name='book_reading_statistics'),
]
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer, BookWithoutFullDescriptionSerializer
from .services import timedelta_to_string, start_reading_session_and_get_message, end_reading_session_and_get_message, \
    get_user_statistics, get_user_reading_statistics


class BookAPIRetrieve(RetrieveAPIView):
    """Displaying information of a specific book by id"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAPIList(ListAPIView):
    """ Displaying a list of all books"""
    queryset = Book.objects.all()
    serializer_class = BookWithoutFullDescriptionSerializer


class StartReadingSessionAPIView(APIView):
    """A class that allows you to start a book reading session"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        response = start_reading_session_and_get_message(user=request.user, book_id=pk)
        return Response(response)


class EndReadingSessionAPIView(APIView):
    """A class that allows you to end a book reading session"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = end_reading_session_and_get_message(user=request.user)
        return Response(response)


class UserStatisticsAPIView(APIView):
    """ Displaying general user statistics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_statistics = get_user_statistics(user=user)

        return Response({
            'Username': user.username,
            'First name': user.first_name,
            'Last name': user.last_name,
            'Date joined': user.date_joined.strftime("%Y-%m-%d %I:%M %p"),
            'Total reading time': timedelta_to_string(user_statistics["total_reading_time"]),
            'Last 7 days reading time': timedelta_to_string(user_statistics["last_7_days_reading_time"]),
            'Last 30 days reading time': timedelta_to_string(user_statistics["last_30_days_reading_time"]),
        })


class ReadingStatisticsAPIView(APIView):
    """Displaying user statistics for a specific book"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        book_id = self.kwargs['pk']

        response = get_user_reading_statistics(user=user, book_id=book_id)
        return Response(response)

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, ReadingSession, ReadingStatistics, UserStatistics
from .serializers import BookSerializer, BookWithoutFullDescriptionSerializer
from .services import end_book_reading_session, timedelta_to_string


class BookAPIRetrieve(RetrieveAPIView):
    """
    Displaying information of a specific book by id
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAPIList(ListAPIView):
    """
    Displaying a list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookWithoutFullDescriptionSerializer


class ReadingSessionAPIView(APIView):
    """
    A class that allows you to start and end a book reading session
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        active_session = ReadingSession.objects.filter(user=request.user, end_time__isnull=True).first()
        if 'pk' in self.kwargs:
            # If pk is in the request, then this is a request to start a reading session
            pk = self.kwargs['pk']

            try:
                book = Book.objects.get(id=pk)
            except Book.DoesNotExist:
                return Response({'Error': 'Book does not exist'})

            if active_session and active_session.book == book:
                response = {'message': 'A reading session for this book is already active'}
            elif active_session:
                end_book_reading_session(active_session.id)
                ReadingSession.objects.create(book=book, user=request.user)
                response = {'message': 'The previous book reading session was ended successfully, '
                                       'and the new book reading session started successfully'}
            elif not active_session:
                ReadingSession.objects.create(book=book, user=request.user)
                response = {'message': 'Book reading session started successfully'}
        else:
            # If pk is not in the request, then this is a request to stop the reading session
            if active_session:
                end_book_reading_session(active_session.id)
                response = {'message': 'Book reading session ended successfully'}
            else:
                response = {'message': 'There is currently no book reading session started'}
        return Response(response)


class UserStatisticsAPIView(APIView):
    """
    Displaying general user statistics
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            user_statistics = user.statistics
        except UserStatistics.DoesNotExist:
            user_statistics = UserStatistics(user=user)
            user_statistics.save()
        total_reading_time = user_statistics.total_reading_time
        last_7_days_reading_time = user_statistics.last_7_days_reading_time
        last_30_days_reading_time = user_statistics.last_30_days_reading_time

        return Response({
            'First name': user.first_name,
            'Last name': user.last_name,
            'Date joined': user.date_joined.strftime("%Y-%m-%d %I:%M %p"),
            'Total reading time': timedelta_to_string(total_reading_time),
            'Last 7 days reading time': timedelta_to_string(last_7_days_reading_time),
            'Last 30 days reading time': timedelta_to_string(last_30_days_reading_time),
        })


class ReadingStatisticsAPIView(APIView):
    """
    Displaying user statistics for a specific book
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        book_id = self.kwargs['pk']

        # Checking whether a book with this ID exists
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
            response = {'details': 'There is no book with this ID'}

        return Response(response)

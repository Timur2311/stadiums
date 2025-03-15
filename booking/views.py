from rest_framework import generics, permissions

from booking.models import Booking
from stadion.models import Stadium

from booking.serializers import BookingSerializer


class BookingRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BookingCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.timezone import localtime, now

from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

import logging

logger = logging.getLogger(__name__)


class FitnessClassViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List only upcoming fitness classes.
    """
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        logger.info("Fetching upcoming fitness classes.")
        queryset = FitnessClass.objects.filter().order_by('datetime')
        logger.debug(f"Found {queryset.count()} upcoming classes.")
        return queryset


class BookClassViewSet(viewsets.ViewSet):
    def create(self, request):
        logger.info("Received booking request.")

        class_id = request.data.get("class_id")
        client_name = request.data.get("client_name")
        client_email = request.data.get("client_email")

        if not all([class_id, client_name, client_email]):
            logger.warning("Booking request missing required fields.")
            return Response({"error": "Enter all the required fields."}, status=400)

        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            logger.error(f"Class with id {class_id} not found.")
            return Response({"error": "Class not found."}, status=404)

        serializer = BookingSerializer(data={
            "fitness_class": fitness_class.id,
            "client_name": client_name,
            "client_email": client_email
        })

        if serializer.is_valid():
            booking = serializer.save()
            logger.info(f"Booking successful for {client_email} in class '{fitness_class.name}'.")
            return Response({"message": "Booking successful"}, status=201)

        logger.warning(f"Booking failed validation: {serializer.errors}")
        return Response(serializer.errors, status=400)


class BookingListViewSet(viewsets.ViewSet):
    def list(self, request):
        email = request.GET.get("email")
        if not email:
            logger.warning("Booking list request missing email parameter.")
            return Response({"error": "Email is required"}, status=400)

        logger.info(f"Fetching bookings for {email}.")
        bookings = Booking.objects.filter(client_email=email).order_by('-booked_at')

        data = [
            {
                "class_name": b.fitness_class.name,
                "date": localtime(b.fitness_class.datetime).strftime('%Y-%m-%d %H:%M'),
                "instructor": b.fitness_class.instructor
            }
            for b in bookings
        ]

        logger.debug(f"Found {len(data)} bookings for {email}.")
        return Response(data)

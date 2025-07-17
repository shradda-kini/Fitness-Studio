from django.utils import timezone
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import FitnessClass, Booking

# Create your tests here.
class FitnessStudioAPITest(APITestCase):

    def setUp(self):
        # Create a fitness class with 2 slots available
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            datetime=timezone.now() + timedelta(days=1),
            instructor="Asha",
            available_slots=2
        )
        self.book_url = reverse('book-list')
        self.classes_url = reverse('class-list')
        self.bookings_url = reverse('bookings-list')

    def test_get_classes_list(self):
        response = self.client.get(self.classes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Yoga")

    def test_post_booking_success(self):
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "user1",
            "client_email": "user1@example.com"
        }
        response = self.client.post(self.book_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Booking successful")

        fc = FitnessClass.objects.get(id=self.fitness_class.id)


    def test_post_booking_fail_no_slots(self):
        # Book max slots
        for i in range(self.fitness_class.available_slots):
            Booking.objects.create(
                fitness_class=self.fitness_class,
                client_name=f"Client{i}",
                client_email=f"client{i}@example.com"
            )
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Client",
            "client_email": "Client@example.com"
        }
        response = self.client.post(self.book_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Class is full.", str(response.data))

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="user1",
            client_email="user1@example.com"
        )
        response = self.client.get(self.bookings_url, {'email': 'user1@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['class_name'], "Yoga")

    def test_get_bookings_no_email(self):
        response = self.client.get(self.bookings_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email is required", str(response.data))

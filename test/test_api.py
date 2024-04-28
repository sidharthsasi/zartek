# tests/test_api.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Rider.models import Ride

class RideAPITest(APITestCase):
    def setUp(self):
        self.ride = Ride.objects.create(
            rider="Sidharth",
            driver="Messi",
            pickup_location="New York",
            dropoff_location="Barcelona",
            status="requested"
        )

    def test_create_ride(self):
        url = reverse('ride_create')
        data = {
            'rider': 'Sidharth',
            'driver': 'Messi',
            'pickup_location': 'New York',
            'dropoff_location': 'Barcelona',
            'status': 'requested'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_rides(self):
        url = reverse('ride_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_ride_details(self):
        url = reverse('ride_detail', args=[self.ride.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ride_status(self):
        url = reverse('ride_status_update', args=[self.ride.id])
        data = {'status': 'started'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

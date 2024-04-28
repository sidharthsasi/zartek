# tests/test_models.py

from django.test import TestCase
from Rider.models import Ride

class RideModelTest(TestCase):
    def test_create_ride(self):
        ride = Ride.objects.create(
            rider="Sidharth",
            driver="Messi",
            pickup_location="New York",
            dropoff_location="Barcelona",
            status="requested"
        )
        self.assertEqual(ride.rider, "Sidharth")
        self.assertEqual(ride.driver, "Messi")
        self.assertEqual(ride.pickup_location, "New York")
        self.assertEqual(ride.dropoff_location, "Barcelona")
        self.assertEqual(ride.status, "requested")

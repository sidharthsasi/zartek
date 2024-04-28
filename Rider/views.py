from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Ride
from .serializers import RideSerializer
from .tasks import update_ride_location
from .utils import calculate_distance
# from django.utils import calculate_distance

# Create your views here.

class RideCreateAPIView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

class RideDetailAPIView(generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

class RideListAPIView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

class RideStartAPIView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        
        # Check if the ride is in a valid state to be started
        if ride.status == 'requested':
            # Update the ride status to 'started'
            ride.status = 'started'
            ride.save()

            # Trigger the Celery task to update the ride's location
            update_ride_location.delay(ride.id, ride.pickup_location)

            return Response({'message': 'Ride started successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ride cannot be started.'}, status=status.HTTP_400_BAD_REQUEST)
        


class RideMatchAPIView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        ride_data = request.data
        pickup_location = ride_data['pickup_location']

        
        available_drivers = Ride.driver.objects.filter(available=True)
        matching_drivers = []
        for driver in available_drivers:
            distance = calculate_distance(driver.current_location, pickup_location)
            if distance < driver.max_pickup_distance:
                matching_drivers.append((driver, distance))

        
        matching_drivers.sort(key=lambda x: x[1])

        if matching_drivers:
            best_match = matching_drivers[0][0]
           
            ride_data['driver'] = best_match.id
            serializer = self.get_serializer(data=ride_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'No available drivers found.'}, status=status.HTTP_404_NOT_FOUND)
        



class RideAcceptAPIView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        ride = self.get_object()

       
        if ride.status == 'requested':
            # Update the ride status to 'accepted'
            ride.status = 'accepted'
            ride.driver = request.user  #  request.user is the authenticated driver
            ride.save()
            return Response({'message': 'Ride accepted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ride cannot be accepted.'}, status=status.HTTP_400_BAD_REQUEST)
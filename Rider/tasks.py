# tasks.py

from celery import shared_task
from .models import Ride
from celery.schedules import crontab
# from .tasks import update_ride_location


@shared_task
def update_ride_location(ride_id, new_location):
    ride = Ride.objects.get(id=ride_id)
    ride.current_location = new_location
    ride.save()

CELERY_BEAT_SCHEDULE = {
    'update_ride_location': {
        'task': 'update_ride_location',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
        # You can adjust the schedule as needed
    },
}
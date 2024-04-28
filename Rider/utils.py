# utils.py

from math import radians, sin, cos, sqrt, atan2

def calculate_distance(location1, location2):
  
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = radians(location1['latitude']), radians(location1['longitude'])
    lat2, lon2 = radians(location2['latitude']), radians(location2['longitude'])

    # Radius of the Earth in kilometers
    R = 6371.0

    # Calculate the differences in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Calculate the distance using the Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

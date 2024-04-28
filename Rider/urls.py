from django.urls import path
from . import views

urlpatterns = [
    path('rides-create/', views.RideCreateAPIView.as_view(), name='ride_create'),
    path('rides-detail/<int:pk>/', views.RideDetailAPIView.as_view(), name='ride_detail'),
    path('rides-list/', views.RideListAPIView.as_view(), name='ride_list'),
    path('rides-start/<int:pk>/', views.RideStartAPIView.as_view(), name='ride_start'),
    path('rides-match/', views.RideMatchAPIView.as_view(), name='ride_match'),
    path('rides-accept/<int:pk>', views.RideAcceptAPIView.as_view(), name='ride_accept'),
]
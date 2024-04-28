from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, status
from .serializers import UserSerializer
from .models import Account




# Create your views here.
# views.py



class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure password is included in request data
        if 'password' not in request.data:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user object with password
        user = Account.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password'),
            email=request.data.get('email')
        )
        
        # Check if user creation was successful
        if user:
            # Create a token for the user
            token_tuple = Token.objects.get_or_create(user=user)
            print(token_tuple)  # Debugging statement
            # Access the token from the tuple
            token = token_tuple[0]
            # Return a success response with the token
            return Response({'token': token.key, 'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to register user'}, status=status.HTTP_400_BAD_REQUEST)





class UserLoginAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Retrieve token associated with the user
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                return Response({'error': 'Token not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        



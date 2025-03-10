from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Note
from .serializers import NoteSerializer,UserSerializer,UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Create your views here.

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            # Ensure response contains data before accessing tokens
            if 'access' not in response.data or 'refresh' not in response.data:
                return Response({'success': False, 'message': 'Token generation failed'}, status=400)

            access_token = response.data['access']
            refresh_token = response.data['refresh']

            res = Response({'success': True})

            # Setting HTTP-only cookies
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,   # Use True in production with HTTPS
                samesite='None',
                path='/'
            )
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            return res  # You must return the response

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=500)


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        Refresh the access token using the refresh token stored in cookies.
        """
        # 🔹 Get refresh token from cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'success': False, 'message': 'No refresh token provided'}, status=400)

        try:
            # 🔹 Validate and create a new access token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # 🔹 Set new access token in cookies
            res = Response({'success': True})
            res.set_cookie('access_token', 
                           access_token, 
                           httponly=True, 
                           secure=True, 
                           samesite='None', 
                           path='/')
            
            return res
        
        except InvalidToken:
            return Response({'success': False, 'message': 'Invalid refresh token'}, status=401)

            
            


@api_view(['POST'])
def logout(request):
    try:
        #  Create an empty response
        res = Response()

        #  Send success response
        res.data = {'success': True}

        #  Delete the access and refresh tokens from cookies
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')

        return res  # Return response with cookies deleted

    except:
        return Response({'success': False}, status=500)  # Return failure response if an error occurs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'authenticated':True})




@api_view(['POST'])
@permission_classes([AllowAny])  # Ensures no authentication is required
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)  




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    user = request.user
    notes= Note.objects.filter(owner=user)
    serializer = NoteSerializer(notes,many=True)

    return Response(serializer.data)
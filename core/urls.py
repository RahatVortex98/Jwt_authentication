from django.urls import path
from .views import get_notes,CustomTokenObtainPairView,CustomTokenObtainPairView, logout,is_authenticated,register
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('get_notes/',get_notes,name='get_notes'),
    path('api/logout/',logout,name='logout'),
    path('api/authenticated/',is_authenticated,name='is_authenticated'),

     path('register/',register,name='register'),



  
]
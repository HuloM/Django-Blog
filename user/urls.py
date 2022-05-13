from django.urls import path, include
from .views import register, TokenObtainPairView

urlpatterns = [
    path('signup', register),
    path('login', TokenObtainPairView.as_view(), name='login')
]

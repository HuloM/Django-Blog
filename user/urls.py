from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register('user', views.UserViewSet)

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/signup/', include('dj_rest_auth.registration.urls'))
    # path('users/<int:id>', views.GenericUserAPIView.as_view()),
    # path('signup/', views.CustomRegisterView.as_view())
]

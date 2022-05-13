from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .serializers import RegisterUserSerializer, TokenObtainLifetimeSerializer, TokenRefreshLifetimeSerializer


@api_view(['PUT'])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'user signed up successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainLifetimeSerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = TokenRefreshLifetimeSerializer



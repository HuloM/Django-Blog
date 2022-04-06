from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	@action(detail=True, methods=['PUT'])
	def update_user(self, request, pk=None):
		response = {'message': 'test'}
		return Response(response, status=status.HTTP_200_OK)
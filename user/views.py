from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# Create your views here.
# TODO add user authentication
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	@parser_classes(JSONParser)
	def create(self, request):
		password = request.data['password']
		confirmPassword = request.data['confirmPassword']

		# TODO check if user with email already exists
		email = request.data['email']

		username = request.data['username']
		first_name = request.data['first_name']
		last_name = request.data['last_name']
		if password != confirmPassword:
			return Response({'post': {
				'username': username,
				'first_name': first_name,
				'last_name': last_name,
				'email': email
			}, 'message': 'User failed to create'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
		# TODO hash password
		user = User(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=''
		)
		user.save()
		return Response({'user': user.as_json(), 'message': 'User created'}, status.HTTP_200_OK)

	@parser_classes(JSONParser)
	def update(self, request, pk=None):
		queryset = User.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		password = request.data['password']
		confirmPassword = request.data['confirmPassword']
		if password != confirmPassword:
			return Response({'message': 'User failed to update'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
		# TODO hash password
		user.password = ''
		user.save()
		return Response({'user': user.as_json(), 'message': 'user updated'}, status.HTTP_200_OK)

	def destroy(self, request, pk=None, **kwargs):
		queryset = User.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		user.delete()
		return Response({'user': user.as_json(), 'message': 'user was deleted'}, status.HTTP_200_OK)

import traceback

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import bcrypt

from .models import User
from .serializers import UserSerializer


# Create your views here.
# TODO add user authentication
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	@action(detail=False, methods=['POST'])
	@parser_classes([JSONParser])
	def login(self, request):
		try:
			email = request.data['email']
			password = request.data['password']
			user = get_object_or_404(self.queryset, email=email)
			print('test')
			# TODO figure out TypeError: Unicode-objects must be encoded before checking on user.password
			if bcrypt.checkpw(password.encode('utf-8'), user.password):
				response = {'message': 'user was logged in', 'user': user.as_json()}
				resStatus = status.HTTP_200_OK
			else:
				response = {'message': 'Password incorrect'}
				resStatus = status.HTTP_401_UNAUTHORIZED
		except:
			traceback.print_exc()
			response = {'message': 'login has failed'}
			resStatus = status.HTTP_422_UNPROCESSABLE_ENTITY
		return Response(response, status=resStatus)

	@parser_classes(JSONParser)
	def create(self, request):
		password = request.data['password']
		confirmPassword = request.data['confirmPassword']

		email = request.data['email']
		user = User.objects.get(email=email)
		if user is not None:
			return Response({'message': 'User with that email already exists'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

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
		user = User(
			username=username,
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
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
		user.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
		user.save()
		return Response({'user': user.as_json(), 'message': 'user updated'}, status.HTTP_200_OK)

	def destroy(self, request, pk=None, **kwargs):
		queryset = User.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		user.delete()
		return Response({'user': user.as_json(), 'message': 'user was deleted'}, status.HTTP_200_OK)

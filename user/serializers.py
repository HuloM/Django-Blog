from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')
		read_only_fields = ('username', 'email')


class RegisterUserSerializer(RegisterSerializer):
	email = serializers.EmailField(required=True)
	username = serializers.CharField(required=True)
	first_name = serializers.CharField(required=True)
	last_name = serializers.CharField(required=True)

	def get_cleaned_data(self):
		super(RegisterUserSerializer, self).get_cleaned_data()

		return {
			'email': self.validated_data.get('email', ''),
			'username': self.validated_data.get('username', ''),
			'password': self.validated_data.get('password1', ''),
			'first_name': self.validated_data.get('first_name', ''),
			'last_name': self.validated_data.get('last_name', '')
		}

	def save(self, request):
		self.cleaned_data = self.get_cleaned_data()
		hashed_password = make_password(self.cleaned_data['password'])
		user = User(
			email=self.cleaned_data['email'],
			username=self.cleaned_data['username'],
			first_name=self.cleaned_data['first_name'],
			last_name=self.cleaned_data['last_name'],
			password=hashed_password
		)
		user.save()
		return user


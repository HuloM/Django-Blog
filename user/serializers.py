from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class RegisterUserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True)
	username = serializers.CharField(required=True)
	first_name = serializers.CharField(required=True)
	last_name = serializers.CharField(required=True)
	password = serializers.CharField(
		write_only=True, required=True, validators=[validate_password])
	confirmPassword = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('email', 'username', 'password', 'confirmPassword', 'first_name', 'last_name')

	# custom validation
	def validate(self, attrs):
		if attrs['password'] != attrs['confirmPassword']:
			raise serializers.ValidationError(
				{'password': 'passwords must match'})

		if User.objects.filter(username=attrs['username']).exists():
			raise serializers.ValidationError(
				{'username': 'User with this username already exists'})

		if User.objects.filter(email=attrs['email']).exists():
			raise serializers.ValidationError(
				{'email': 'This email is already registered with us, please login'})

		return attrs

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		confirmPassword = validated_data.pop('confirmPassword', None)
		# as long as the fields are the same, we can just use this
		post = self.Meta.model(**validated_data)
		if password is not None:
			post.set_password(password)
		post.save()
		return post


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

	def validate(self, attrs):
		data = super().validate(attrs)
		refresh = self.get_token(self.user)
		# renaming access key to token to avoid chaning frontend for django specific
		data['token'] = data.pop('access')
		# setting additional keys to provide necessary information for frontend
		data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
		data['userId'] = self.user.id
		data['username'] = self.user.username
		return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

	def validate(self, attrs):
		data = super().validate(attrs)
		refresh = RefreshToken(attrs['refresh'])
		data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
		return data
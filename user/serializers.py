from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework import serializers


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

	def validate(self, attrs):
		if attrs['password'] != attrs['confirmPassword']:
			raise serializers.ValidationError(
				{'password': 'Password fields didn\'t match.'})

		if User.objects.filter(username=attrs['username']).exists():
			raise serializers.ValidationError(
				{'username': 'User with this username already exists.'})

		if User.objects.filter(email=attrs['email']).exists():
			raise serializers.ValidationError(
				{'email': 'User with this email already exists.'})

		return attrs

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		confirmPassword = validated_data.pop('confirmPassword', None)
		# as long as the fields are the same, we can just use this
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

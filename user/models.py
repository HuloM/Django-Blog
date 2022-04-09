import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import CustomUserManager


# Create your models here.
class User(AbstractBaseUser):
	email = models.EmailField(verbose_name='email', max_length=50, unique=True)
	username = models.CharField(max_length=25, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

	objects = CustomUserManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def as_json(self):
		return dict(
			id=self.id,
			uuid=self.uuid,
			username=self.username or None,
			name=(self.first_name + ' ' + self.last_name) or None,
			email=self.email or None
		)

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

	def as_json(self):
		return dict(
			id=self.id,
			uuid=self.uuid,
			username=self.username or None,
			name=(self.first_name + ' ' + self.last_name) or None,
			email=self.email or None
		)

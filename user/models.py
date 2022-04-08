import uuid

from django.db import models


# Create your models here.
class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)

	def as_json(self):
		return dict(
			id=self.id,
			username=self.username or None,
			name=(self.first_name + ' ' + self.last_name) or None,
			email=self.email or None
		)

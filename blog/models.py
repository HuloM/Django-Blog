import uuid

from django.conf import settings
from django.db import models


# Create your models here.
class Post(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images', null=True)
	body = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	slug = models.SlugField(max_length=100, editable=False)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')

	def as_json(self):
		return dict(
			id=self.id,
			uuid=self.uuid,
			title=self.title,
			image=str(self.image.url),
			body=self.body,
			date_created=self.date_created,
			date_updated=self.date_created,
			slug=self.slug,
			author=self.author.as_json()
		)


class Comment(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	comment = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')

	def as_json(self):
		return dict(
			id=self.id,
			comment=self.comment,
			author=self.author.as_json(),
			post=self.post.as_json()
		)

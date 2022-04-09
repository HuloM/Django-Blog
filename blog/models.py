import uuid

from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images', null=True)
	body = models.TextField()
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)
	slug = models.SlugField(max_length=100, editable=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

	def as_json(self):
		return dict(
			id=self.id,
			title=self.title or None,
			image=str(self.image.url) or None,
			body=self.body or None,
			date_created=self.date_created or None,
			date_updated=self.date_created or None,
			slug=self.slug or None,
			author=self.author.as_json() or None
		)


class Comment(models.Model):
	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	comment = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author', null=True, default=None)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post', null=True, default=None)

	def as_json(self):
		return dict(
			id=self.id,
			comment=self.comment or None,
			author=self.author.as_json() or None,
			post=self.post.as_json() or None
		)

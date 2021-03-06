from django.conf import settings
from django.db import models


# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images', null=True)
	body = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	# this will use the default django user model as the model
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')

	# when a detailed post is needed
	def as_json(self):
		return dict(
			id=self.id,
			title=self.title,
			imageUrl=str(self.image.url),
			body=self.body,
			createdAt=self.date_created,
			author=self.author.as_json(),
			comments=[comment.as_json() for comment in self.comments.filter(post_id=self.id)],
		)

	# when a less detailed list of posts is needed
	def list_json(self):
		return dict(
			id=self.id,
			title=self.title,
			createdAt=self.date_created,
			author=self.author.as_json()
		)


class Comment(models.Model):
	comment = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

	def as_json(self):
		return dict(
			id=self.id,
			comment=self.comment,
			author=self.author.as_json(),
		)

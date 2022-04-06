from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images', null=True)
	body = models.TextField()
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)
	slug = models.SlugField(max_length=100)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', null=True, default=None)

	def as_json(self):
		return dict(
			id=self.id,
			title=self.title or None,
			image=self.image or None,
			body=self.body or None,
			date=self.date or None,
			slug=self.slug or None,
			author=self.author or None
		)

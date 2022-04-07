from django.utils.text import slugify
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'

	# DELETE: http://localhost:8000/blog/posts/<id>/ body = None
	# PUT: http://localhost:8000/blog/posts/<id>/ body = {title, image, body, author}
	# POST: http://localhost:8000/blog/posts/ body = {title, image, body, author}
	# GET: http://localhost:8000/blog/posts/
	# GET single object: http://localhost:8000/blog/posts/<id>/ body = None
	# IMAGES can be found: http://localhost:8000/user-media/images/<image file>

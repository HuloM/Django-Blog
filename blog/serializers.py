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
	def create(self, validated_data):
		post = Post(
			title=validated_data['title'],
			image=validated_data['image'],
			body=validated_data['body'],
			slug=slugify(validated_data['title']),
			author=validated_data['author'] or None
		)
		post.save()
		return post

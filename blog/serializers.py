from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = '__all__'

	# GET single object: http://localhost:8000/blog/post/<id>/ body = None
	# DELETE: http://localhost:8000/blog/post/<id>/ body = None
	# PUT: http://localhost:8000/blog/post/<id>/ body = {title, image, body, author}

	# POST: http://localhost:8000/blog/posts/ body = {title, image, body, author}
	# GET: http://localhost:8000/blog/posts/

	# IMAGES can be found: http://localhost:8000/user-media/images/<image file>


class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = '__all__'

	# POST: http://localhost:8000/blog/post/comments body = {postId}

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# Create your views here.
class PostsViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request, **kwargs):
		return Response({'message': 'wrong endpoint for this action try GET request with /posts/<page>'},
						status.HTTP_405_METHOD_NOT_ALLOWED)

	def retrieve(self, request, pk=None, **kwargs):
		# returning all posts (this can be a good place to add pagination)
		posts = self.queryset

		p = Paginator([post.list_json() for post in posts], 3)
		return Response({'posts': p.page(pk).object_list, 'message': 'list of posts retrieved'}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def create(self, request):
		if type(request.user) is AnonymousUser:
			return Response({'message': 'not authorized'}, status.HTTP_401_UNAUTHORIZED)
		# when sending a post request, django will store that in
		# request.data with the name of form items being keys
		if 'image' not in request.FILES:
			return Response({'message': 'No image uploaded'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
		if request.FILES['image'].split('.')[1] not in ['png', 'jpeg', 'jpg']:
			return Response({'message': 'incorrect file type submitted (accepted: PNG, JPG, JPEG)'},
							status.HTTP_422_UNPROCESSABLE_ENTITY)

		post = Post(
			title=request.data['title'],
			image=request.FILES['image'],
			body=request.data['body'],
			author=request.user
		)
		# .save() is a method that django dynamically makes to save model
		# objects
		post.save()
		# returning JSON with post data and status code
		return Response({'post': post.as_json(), 'message': 'Post created'}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def update(self, request, pk=None):
		return Response({'message': 'wrong endpoint for this action try PUT request with /post/<postId>'},
						status.HTTP_405_METHOD_NOT_ALLOWED)

	def destroy(self, request, pk=None, **kwargs):
		return Response({'message': 'wrong endpoint for this action try DELETE request with /post/<postId>'},
						status.HTTP_405_METHOD_NOT_ALLOWED)


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request, **kwargs):
		return Response({'message': 'wrong endpoint for this action try GET request with /posts/<page>'},
						status.HTTP_405_METHOD_NOT_ALLOWED)

	@parser_classes(MultiPartParser)
	def create(self, request):
		return Response({'message': 'wrong endpoint for this action try POST request with /posts/'},
						status.HTTP_405_METHOD_NOT_ALLOWED)

	def retrieve(self, request, pk=None, **kwargs):
		# .objects and .objects.all() are dynamically made by django
		# and will result in returning the entire list of rows

		post = get_object_or_404(self.queryset, pk=pk)
		return Response({'post': post.as_json(), 'message': 'single post retrieved'}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def update(self, request, pk=None):
		if type(request.user) is AnonymousUser:
			return Response({'message': 'not authorized'}, status.HTTP_401_UNAUTHORIZED)
		# similar to retrieve we get the whole list and then look for the
		# one that matches the pk we passed
		queryset = Post.objects.all()
		post = get_object_or_404(queryset, pk=pk)

		# user authentication to see if post author is the user
		if post.author == request.user:
			storage, path, image = post.image.storage, post.image.path, str(post.image).split('/')[1]
			# checking if the user passed in a new image
			if 'image' in request.FILES:
				print(request.FILES['image'].name.split('.')[1])
				if request.FILES['image'].name.split('.')[1].lower() not in ['png', 'jpeg', 'jpg']:
					return Response({'message': 'incorrect file type submitted (accepted: PNG, JPG, JPEG)'},
									status.HTTP_422_UNPROCESSABLE_ENTITY)
				storage.delete(path)
				post.image = request.FILES['image']

			post.title = request.data['title'] or post.title
			post.body = request.data['body'] or post.body
			# after changing the wanted variables we call .save() to update the database
			post.save()
			return Response({'post': post.as_json(), 'message': 'post updated'}, status.HTTP_200_OK)
		else:
			return Response({'message': 'user is not author of post'}, status.HTTP_401_UNAUTHORIZED)

	def destroy(self, request, pk=None, **kwargs):
		if type(request.user) is AnonymousUser:
			return Response({'message': 'not authorized'}, status.HTTP_401_UNAUTHORIZED)

		queryset = Post.objects.all()
		post = get_object_or_404(queryset, pk=pk)
		# user authentication to see if post author is the user
		if post.author is request.user:
			# deleting the image before we delete the post
			storage, path = post.image.storage, post.image.path
			storage.delete(path)
			# .delete() is another method django makes to delete rows
			post.delete()
			return Response({'post': post.as_json(), 'message': 'Post deleted Successfully'}, status.HTTP_200_OK)
		else:
			return Response({'message': 'user is not author of post'}, status.HTTP_401_UNAUTHORIZED)


class CommentsViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def list(self, request, **kwargs):
		comments = self.queryset
		return Response(
			{
				'posts': [comment.as_json() for comment in comments],
				'message': 'list of comments retrieved'
			}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def create(self, request):
		if type(request.user) is AnonymousUser:
			return Response({'message': 'not authorized'}, status.HTTP_401_UNAUTHORIZED)
		post = get_object_or_404(Post.objects.all(), pk=request.data['postId'])

		comment = Comment(
			comment=request.data['comment'],
			post=post,
			author=request.user
		)
		comment.save()
		return Response({'comment created'}, status.HTTP_200_OK)

	def retrieve(self, request, pk=None, **kwargs):
		return Response({'message': 'A comment may not be retrieved like this'}, status.HTTP_405_METHOD_NOT_ALLOWED)

	# preventing user from trying to update comment
	def update(self, request, pk=None, **kwargs):
		return Response({'message': 'A comment may not be changed once posted'}, status.HTTP_405_METHOD_NOT_ALLOWED)

	# preventing user from trying to delete comment
	def destroy(self, request, pk=None, **kwargs):
		return Response({'message': 'A comment may not be deleted once posted'}, status.HTTP_405_METHOD_NOT_ALLOWED)

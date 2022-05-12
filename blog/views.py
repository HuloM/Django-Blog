from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Post, Comment
from .serializers import PostSerializer


# Create your views here.
class PostsViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request, **kwargs):
		# returning all posts (this can be a good place to add pagination)
		posts = self.queryset

		p = Paginator([post.list_json() for post in posts], 4)
		return Response({'posts': p.page(request.data['page'] or 1), 'message': 'list of posts retrieved'}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def create(self, request):
		if type(request.user) is AnonymousUser:
			return Response({'message': 'not authorized'}, status.HTTP_401_UNAUTHORIZED)
		# when sending a post request, django will store that in
		# request.data with the name of form items being keys
		print('made it past')
		post = Post(
			title=request.data['title'],
			image=request.data['image'],
			body=request.data['body'],
			author=request.user
		)
		# .save() is a method that django dynamically makes to save model
		# objects
		post.save()
		# returning JSON with post data and status code
		return Response({'post': post.as_json(), 'message': 'Post created'}, status.HTTP_200_OK)

	def retrieve(self, request, pk=None, **kwargs):
		# .objects and .objects.all() are dynamically made by django
		# and will result in returning the entire list of rows
		queryset = Post.objects.all()

		# .objects and .objects.all() are dynamically made by django
		# and will result in returning the entire list of rows

		post = get_object_or_404(queryset, pk=pk)
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
		if post.author is request.user:
			storage, path, image = post.image.storage, post.image.path, str(post.image).split('/')[1]
			post.title = request.data['title'] or post.title
			# checking if the user passed in a new image
			if request.data['image']:
				# we can mutate the post objects fields by just setting
				# new variables to them
				post.title = request.data['title'] or post.title
				# checking if the user passed in a new image

				if str(post.image) != image:
						storage.delete(path)
				post.body = request.data['body'] or post.body
				post.slug = slugify(request.data['title'] or post.title)
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
			return Response({'post': post.as_json(), 'message': 'post was deleted'}, status.HTTP_200_OK)
		else:
			return Response({'message': 'user is not author of post'}, status.HTTP_401_UNAUTHORIZED)


class CommentsViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = PostSerializer

	def list(self, request, **kwargs):
		comments = Comment.objects.all()
		return Response(
			{
				'posts': [comment.as_json() for comment in comments],
				'message': 'list of comments retrieved'
			 }, status.HTTP_200_OK)

	@parser_classes(JSONParser)
	def create(self, request):
		if type(request.user) is AnonymousUser:
			return Response({'message': 'not authorized'}, status.HTTP_401_UNAUTHORIZED)

		comment = Comment(
			comment=request.data['comment'],
			post=request.data['post'],
			author=request.user
		)
		comment.save()
		return Response({'comment created'}, status.HTTP_200_OK)

	def retrieve(self, request, pk=None, **kwargs):
		queryset = Comment.objects.all()
		comment = get_object_or_404(queryset, pk=pk)
		return Response({'post': comment.as_json(), 'message': 'single comment retrieved'}, status.HTTP_200_OK)

	# preventing user from trying to update comment
	def update(self, request, pk=None, **kwargs):
		return Response({'message': 'A comment may not be changed once posted'}, status.HTTP_401_UNAUTHORIZED)

	# preventing user from trying to delete comment
	def destroy(self, request, pk=None, **kwargs):
		return Response({'message': 'A comment may not be deleted once posted'}, status.HTTP_401_UNAUTHORIZED)


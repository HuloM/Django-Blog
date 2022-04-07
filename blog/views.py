from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import viewsets, status
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostsViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def list(self, request, **kwargs):
		posts = Post.objects.all()
		return Response({'posts': [post.as_json() for post in posts], 'message': 'list of posts retrieved'}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def create(self, request):
		post = Post(
			title=request.data['title'],
			image=request.data['image'],
			body=request.data['body'],
			slug=slugify(request.data['title']),
			author=request.data['author'] or None
		)
		post.save()
		return Response({'post': post.as_json(), 'message': 'Post created'}, status.HTTP_200_OK)

	def retrieve(self, request, pk=None, **kwargs):
		queryset = Post.objects.all()
		post = get_object_or_404(queryset, pk=pk)
		return Response({'post': post.as_json(), 'message': 'single post retrieved'}, status.HTTP_200_OK)

	@parser_classes(MultiPartParser)
	def update(self, request, pk=None):
		queryset = Post.objects.all()
		post = get_object_or_404(queryset, pk=pk)
		storage, path, image = post.image.storage, post.image.path, str(post.image).split('/')[1]
		post.title = request.data['title'] or post.title

		if request.data['image']:
			post.image = request.data['image'] or path.image
			if str(post.image) != image:
				storage.delete(path)
		post.body = request.data['body'] or post.body
		post.slug = slugify(request.data['title'] or post.title)
		post.save()
		return Response({'post': post.as_json(), 'message': 'post updated'}, status.HTTP_200_OK)

	def destroy(self, request, pk=None, **kwargs):
		queryset = Post.objects.all()
		post = get_object_or_404(queryset, pk=pk)
		storage, path = post.image.storage, post.image.path
		print(storage, path, post.image)
		storage.delete(path)
		post.delete()
		return Response({'post': post.as_json(), 'message': 'post was deleted'}, status.HTTP_200_OK)


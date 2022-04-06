import json

from django.utils.text import slugify
from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostsViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	@action(detail=True, methods=['PUT'])
	@parser_classes([JSONParser])
	def update_blog(self, request, pk=None):
		try:
			reqBody = request.data
			post = Post.objects.get(id=pk)
			post.title = reqBody['title']
			# TODO include image URL change
			post.body = reqBody['body']
			post.slug = slugify(reqBody['title'])
			post.save()
			response = {'message': 'post was updated', 'post': post.as_json()}
			resStatus = status.HTTP_200_OK
		except:
			response = {'message': 'post has failed'}
			resStatus = status.HTTP_422_UNPROCESSABLE_ENTITY
		return Response(response, status=resStatus)


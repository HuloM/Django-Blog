import json
import traceback

from django.utils.text import slugify
from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostsViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	@action(detail=True, methods=['PUT'])
	@parser_classes([MultiPartParser])
	def update_post(self, request, pk=None):
		try:
			reqBody = request.data
			print(reqBody)
			post = Post.objects.get(id=pk)
			post.title = reqBody['title']
			print('cleared')
			if reqBody['image'] is not None:
				post.image = reqBody['image']
			print(post.image)
			post.body = reqBody['body']
			print('cleared')
			post.slug = slugify(reqBody['title'])
			print('cleared')
			post.save()
			print('saved')
			response = {'message': 'post was updated', 'post': post.as_json()}
			resStatus = status.HTTP_200_OK
		except:
			traceback.print_exc()
			response = {'message': 'post has failed'}
			resStatus = status.HTTP_422_UNPROCESSABLE_ENTITY
		return Response(response, status=resStatus)

	@action(detail=True, methods=['DELETE'])
	def delete_post(self, request, pk=None):
		try:
			post = Post.objects.get(id=pk)
			response = {'message': 'post was delete', 'post': post.as_json()}
			post.delete()
			resStatus = status.HTTP_200_OK
		except:
			traceback.print_exc()
			response = {'message': 'post has failed'}
			resStatus = status.HTTP_422_UNPROCESSABLE_ENTITY
		return Response(response, status=resStatus)


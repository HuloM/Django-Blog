from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# GET, POST http://localhost:8000/posts/
# GET, PUT, DELETE http://localhost:8000/post/<id>
# POST http://localhost:8000/post/comments/
router.register('posts', views.PostsViewSet)
router.register('post/comments', views.CommentsViewSet)
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]

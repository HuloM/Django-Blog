from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# GET, POST http://localhost:8000/posts/
# PUT, DELETE http://localhost:8000/posts/<id>
router.register('posts', views.PostsViewSet)
router.register('posts/comments', views.CommentsViewSet)

urlpatterns = [
    path('', include(router.urls))
]

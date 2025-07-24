from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls), name='posts_viewset'),
]

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TweetViewSet

app_name = 'tweets'


router = DefaultRouter()
router.register(r'tweets', TweetViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework.routers import DefaultRouter
from .views import FollowViewSet, LikeViewSet
from django.urls import path, include

app_name = 'interactions'



router = DefaultRouter()
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'likes', LikeViewSet, basename='like')




urlpatterns = [
    path('', include(router.urls)),
] 

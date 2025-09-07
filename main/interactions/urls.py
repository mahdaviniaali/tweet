from rest_framework.routers import DefaultRouter
from .views import FollowViewSet
from django.urls import path, include

app_name = 'interactions'


router = DefaultRouter()
router.register(r'follows', FollowViewSet, basename='follow')




urlpatterns = [
    path('', include(router.urls)),
] 

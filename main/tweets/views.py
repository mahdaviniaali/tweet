from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tweet
from interactions.models import Follow
from .serializers import TweetSerializer
from django.utils import timezone
from rest_framework.permissions import BasePermission
# Create your views here.

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.user == request.user


class TweetViewSet(viewsets.ModelViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


    def get_queryset(self):
        following_users= Follow.objects.user_following_of(user=self.request.user).values_list("following", flat=True)
        today = timezone.now().date()
        #return Tweet.objects.filter(user_id__in=following_users, created_at__date=today)
        return Tweet.objects.all()
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def retweet(self, request, pk=None):
        original_tweet = get_object_or_404(Tweet, pk=pk)
        tweet = Tweet.objects.create(
            user=request.user,
            content=original_tweet.content,
            retweet=original_tweet
        )
        serializer = self.get_serializer(tweet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




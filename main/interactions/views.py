from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import Follow, Like
from .serializers import FollowSerializer, LikeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        following = serializer.validated_data.get('following')
        if following == self.request.user:
            from django.core.exceptions import ValidationError
            raise ValidationError("cannot follow yourself")
        serializer.save(follower=self.request.user)


    @action(detail=False, methods=["get"])
    def followers(self, request):
        user_id = request.query_params.get("user_id", request.user.id)
        user = get_object_or_404(User, pk=user_id)
        qs = Follow.objects.user_following_of(user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=["get"])
    def following(self, request):
        user_id = request.query_params.get("user_id", request.user.id)
        user = get_object_or_404(User, pk=user_id)
        qs = Follow.objects.user_following_of(user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=["post"])
    def follow(self, request):
        user_to_follow_id = request.data.get("user_id")
        if not user_to_follow_id:
            return Response({"error": "user_id is required"}, status=400)

        user_to_follow = get_object_or_404(User, pk=user_to_follow_id)

        try:
            follow = Follow.objects.follow(request.user, user_to_follow)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        except IntegrityError:
            return Response({"status": "already following"})

        serializer = self.get_serializer(follow)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def unfollow(self, request):
        user_to_unfollow_id = request.data.get("user_id")
        if not user_to_unfollow_id:
            return Response({"error": "user_id is required"}, status=400)

        user_to_unfollow = get_object_or_404(User, pk=user_to_unfollow_id)
        deleted, _ = Follow.objects.unfollow(request.user, user_to_unfollow)

        if deleted:
            return Response({"status": "unfollowed"})
        return Response({"status": "not following"}, status=400)



class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        from tweets.models import Tweet
        tweet = get_object_or_404(Tweet, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            return Response({"detail": "Already liked."}, status=400)
        serializer = self.get_serializer(like)
        return Response(serializer.data)

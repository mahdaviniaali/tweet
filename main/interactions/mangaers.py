from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowManager(models.Manager):
    def for_user(self, user):
        return self.filter(follower=user)

    def followers_of(self, user):
        return self.filter(following=user)

    def following_of(self, user):
        return self.filter(follower=user)

    def follow(self, follower, following):
        if follower == following:
            raise ValidationError("cannot follow yourself")
        return self.create(follower=follower, following=following)

    def unfollow(self, follower, following):
        return self.filter(follower=follower, following=following).delete()

    def user_following_of(self, user):
        """
        کاربرهایی که این یوزر فالو کرده
        """
        return User.objects.filter(
            followers_relation__follower=user
        )

    def user_followers_of(self, user):
        """
        کاربرهایی که این یوزر رو فالو کردن
        """
        return User.objects.filter(
            following_relation__following=user
        )
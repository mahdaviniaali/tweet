from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


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


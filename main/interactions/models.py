from main.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model
from .mangaers import FollowManager
User = get_user_model()
# Create your models here.

class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_relation")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_relation")
    created_at = models.DateTimeField(auto_now_add=True)


    objects = FollowManager()
    def __str__(self):
        return f"{self.follower} -> {self.following}"


    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("tweets.Tweet", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.tweet}"

    class Meta:
        unique_together = ("user", "tweet")
        ordering = ["-created_at"]
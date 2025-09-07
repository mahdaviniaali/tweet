from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_rel")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_rel")
    class Meta:
        unique_together = ("follower", "following")

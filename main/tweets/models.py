from django.db import models
from main.models import BaseModel
# Create your models here.

class Tweet(BaseModel):
    content = models.TextField(max_length=280)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="tweets")
    retweet=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="retweets")
    def __str__(self):
        return f"{self.user}: {self.content[:50]}"

    class Meta:
        ordering = ["-created_at"]
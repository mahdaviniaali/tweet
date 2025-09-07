from rest_framework import serializers
from .models import Tweet
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]  


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  
    retweet = serializers.SerializerMethodField() 

    class Meta:
        model = Tweet
        fields = ["id", "content", "user", "retweet", "created_at"]

    def get_retweet(self, obj):

        if obj.retweet:
            return {
                "id": obj.retweet.id,
                "content": obj.retweet.content,
                "user": {
                    "id": obj.retweet.user.id,
                    "username": obj.retweet.user.username
                },
                "created_at": obj.retweet.created_at
            }
        return None

from rest_framework import serializers
from .models import ImagePost
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class ImagePostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username', read_only=True)
    likers = serializers.SerializerMethodField()

    def get_likers(self, obj):
        return obj.likes.all().values_list("likes__user__username", flat=True)

    class Meta:
        model = ImagePost
        fields = ['id', 'user', 'author', 'caption', 'created_on',
                  'image_url', 'likes', 'public', 'likers']
        read_only_fields = ['user', 'created_on']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        print(password)
        user = User.objects.create_user(
            validated_data['username'],
        )
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]
        # read_only_fields = [""]

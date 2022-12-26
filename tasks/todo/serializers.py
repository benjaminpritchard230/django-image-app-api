from rest_framework import serializers
from .models import ImagePost, Comment
from django.contrib.auth import get_user_model
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ImagePostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.username', read_only=True)
    image_url = serializers.ImageField(required=False)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    liked_by = serializers.StringRelatedField(
        many=True, source="likes", read_only=True)

    class Meta:
        model = ImagePost
        fields = "__all__"
        read_only_fields = ['id', 'user', 'author', 'created_on', 'image_url']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    post = serializers.IntegerField(source='post.id', read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    liked_by = serializers.StringRelatedField(
        many=True, source="likes", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        print(password)
        user = get_user_model().objects.create_user(
            validated_data['username'],
        )
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        read_only_fields = ["username", "is_staff", "is_active",
                            "date_joined", "user_permissions", "groups", "last_login", "id", ]
        exclude = ("password", "first_name", "email", "groups",
                   "last_name", "is_superuser", "is_staff", "user_permissions")


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["username", "id", ]

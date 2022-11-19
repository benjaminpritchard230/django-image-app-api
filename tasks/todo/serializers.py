from rest_framework import serializers
from .models import ImagePost
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'user', 'caption', 'created_on', ]
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

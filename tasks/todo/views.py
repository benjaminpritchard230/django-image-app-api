from django.http import JsonResponse
from .models import ImagePost, User
from .serializers import ImagePostSerializer, CreateUserSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


# Class based api view for getting the list of ImagePosts corresponding
# to a token or posting a new ImagePost to a specific user's ImagePost list


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class LikePostView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id, format=None):
        try:
            post = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)


class AllImagePostsView(APIView, LimitOffsetPagination):
    """Class based api view for showing all public image posts regardles of whether user is logged in."""

    def get(self, request, format=None):
        if request.method == "GET":
            posts = ImagePost.objects.filter(public=True)
            results = self.paginate_queryset(posts, request, view=self)
            serializer = ImagePostSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)


class ListImagePostsView(APIView):
    """Class based api view for getting the list of ImagePosts corresponding 
    to a token or posting a new ImagePost to a specific user's ImagePost list"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if request.method == "GET":
            ImagePosts = ImagePost.objects.filter(user=self.request.user)
            serializer = ImagePostSerializer(ImagePosts, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImagePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            print(self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificImagePostView(APIView):
    """Class based  api view for getting a specific ImagePost based on ID, putting new
    information for a ImagePost with a specific ID or deleting a ImagePost with a specific ID"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            post = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.user == self.request.user:
            serializer = ImagePostSerializer(post)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id, format=None):
        try:
            post = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImagePostSerializer(post, data=request.data)
        if post.user == self.request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id, format=None):
        try:
            post = ImagePost.objects.get(pk=id)

        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.user == self.request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(APIView):
    """Class based api view for registering a new user with a username and password"""

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, safe=False)


class UserInfoView(APIView):
    """Class based api view to get information about a specific user"""

    def get(self, request, id, format=None):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

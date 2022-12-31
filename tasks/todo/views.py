from django.http import JsonResponse
from .models import ImagePost, Comment
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from notifications.signals import notify
from notifications.models import *
from notifications_rest.serializers import *


# Class based api view for getting the list of ImagePosts corresponding
# to a token or posting a new ImagePost to a specific user's ImagePost list


class CustomObtainAuthToken(ObtainAuthToken):
    """Api view for getting token."""

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        username = str(token.user)
        print(token.user)
        return Response({'token': token.key, 'id': token.user_id, "username": username})


class LikePostView(APIView):
    """Api view for liking a post if logged in."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id, format=None):
        user = request.user
        try:
            post = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            if user != post.user:
                notify.send(user, recipient=post.user,
                            verb=f"{user.username} liked your post.")
        return Response(status=status.HTTP_200_OK)


class AllImagePostsView(APIView, PageNumberPagination):
    """Class based api view for showing all public image posts regardles of whether user is logged in."""

    def get(self, request, format=None):
        posts = ImagePost.objects.filter(public=True)
        results = self.paginate_queryset(posts, request, view=self)
        serializer = ImagePostSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class UserFollowingPostsView(APIView):
    """Class based api view for showing image posts posted by people user is following."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        def get_queryset(self):
            following = request.user.following.all()
            following_posts = ImagePost.objects.filter(
                user__in=following, public=True)
            return following_posts
        serializer = ImagePostSerializer(get_queryset(self), many=True)
        return Response(data=serializer.data)


class ListImagePostsView(APIView):
    """Class based api view for getting the list of ImagePosts corresponding
    to a token or posting a new ImagePost to a specific user's ImagePost list"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        ImagePosts = ImagePost.objects.filter(user=request.user)
        serializer = ImagePostSerializer(ImagePosts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImagePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            print(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LikeCommentView(APIView):
    """Class based api view for liking/unliking comments"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id, format=None):
        user = request.user
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if comment.likes.filter(pk=request.user.pk).exists():
            comment.likes.remove(request.user)

        else:
            comment.likes.add(request.user)
            if user != comment.user:
                notify.send(user, recipient=comment.user,
                            verb=f"{user.username} liked your comment.")
        return Response(status=status.HTTP_200_OK)


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
        if post.user == request.user:
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
        if post.user == request.user:
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
        if post.user == request.user:
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
            user = get_user_model().objects.get(pk=id)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class EditUserInfoView(APIView):
    """API View for editing user info of currently logged in user."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            user = request.user
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# class FollowUserView(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def put(self, request, id, format=None):
#         try:
#             post = ImagePost.objects.get(pk=id)
#         except ImagePost.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         if post.likes.filter(pk=request.user.pk).exists():
#             post.likes.remove(request.user)
#         else:
#             post.likes.add(request.user)
#         return Response(status=status.HTTP_200_OK)


class ListUserPostsView(APIView):
    """Class based api view for getting the list of ImagePosts made by a specific user"""

    def get(self, request, id, format=None):
        try:
            user = get_user_model().objects.get(pk=id)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        posts = ImagePost.objects.filter(user=user).filter(public=True)

        serializer = ImagePostSerializer(posts, many=True)
        return Response(serializer.data)


class AddImagePostCommentView(APIView):
    """Class based api view for adding a new comment to a post, whilst authorised."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, format=None):
        user = request.user
        print(request.data)
        try:
            post = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            if user != post.user:
                notify.send(user, recipient=post.user,
                            verb=f"{user.username} commented on your post.")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class GetImagePostCommentsView(APIView):
    """Class based api view for getting all of the comments associated with a post."""

    def get(self, request, id, format=None):
        try:
            post = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class FollowUserView(APIView):
    """Class based api view for following other users whilst logged in."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id, format=None):
        user = request.user
        try:
            other_user = get_user_model().objects.get(pk=id)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user.following.filter(pk=other_user.pk).exists():
            request.user.following.remove(other_user)
        else:
            request.user.following.add(other_user)
            if user != other_user:
                notify.send(user, recipient=other_user,
                            verb=f"{user.username} is now following you.")
        return Response(status=status.HTTP_200_OK)


class SpecificCommentView(APIView):
    """Class based  api view for getting a specific Comment based on ID, putting new
    information for a Comment with a specific ID or deleting a Comment with a specific ID"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if comment.user == request.user:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id, format=None):
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment, data=request.data)
        if comment.user == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id, format=None):
        try:
            comment = Comment.objects.get(pk=id)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if comment.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListMyNotificationsView(APIView):
    """Class based api view for getting the list of ImagePosts corresponding
    to a token or posting a new ImagePost to a specific user's ImagePost list"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.filter(recipient=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class SpecificNotificationView(APIView):
    """Class based api view for getting the list of ImagePosts corresponding
    to a token or posting a new ImagePost to a specific user's ImagePost list"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        notification = Notification.objects.filter(pk=id)
        serializer = NotificationSerializer(notification, many=True)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        try:
            notification = Notification.objects.get(pk=id)
        except notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateNotificationSerializer(
            notification, data=request.data)
        if notification.recipient == self.request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

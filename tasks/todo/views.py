from django.http import JsonResponse
from .models import ImagePost
from .serializers import ImagePostSerializer, CreateUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Class based api view for getting the list of ImagePosts corresponding
# to a token or posting a new ImagePost to a specific user's ImagePost list


class ListImagePosts(APIView):
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


class SpecificImagePost(APIView):
    """Class based  api view for getting a specific ImagePost based on ID, putting new
    information for a ImagePost with a specific ID or deleting a ImagePost with a specific ID"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            ImagePost = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if ImagePost.user == self.request.user:
            serializer = ImagePostSerializer(ImagePost)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id, format=None):
        try:
            ImagePost = ImagePost.objects.get(pk=id)
        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImagePostSerializer(ImagePost, data=request.data)
        if ImagePost.user == self.request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id, format=None):
        try:
            ImagePost = ImagePost.objects.get(pk=id)

        except ImagePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if ImagePost.user == self.request.user:
            ImagePost.delete()
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

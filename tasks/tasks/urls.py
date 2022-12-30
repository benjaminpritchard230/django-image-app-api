"""tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
import notifications.urls
import notifications_rest.urls

app_name = 'tasks'
urlpatterns = [
    path('admin/', admin.site.urls),
    # Api views
    # Auth views
    path('login/', CustomObtainAuthToken.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
    # User urls
    path("user/<int:id>/", UserInfoView.as_view(), name="user_profile"),
    path("user/<int:id>/follow/", FollowUserView.as_view(), name="follow_user"),
    path("user/<int:id>/posts/", ListUserPostsView.as_view(), name="user_posts"),
    path("user/", EditUserInfoView.as_view(), name="edit_user"),
    # Post urls
    path('posts/<int:id>/', SpecificImagePostView.as_view(), name="specific_image"),
    path('posts/my/', ListImagePostsView.as_view(), name="my_posts"),
    path('posts/all/', AllImagePostsView.as_view(), name='all_posts'),
    path("posts/<int:id>/like/", LikePostView.as_view(), name="like"),
    path("posts/following/", UserFollowingPostsView.as_view(),
         name="following_posts"),
    # Comments urls
    path('posts/<int:id>/comments/',
         GetImagePostCommentsView.as_view(), name="post_comments"),
    path('posts/<int:id>/comments/add/',
         AddImagePostCommentView.as_view(), name="add_comment"),
    path("comments/<int:id>/like/", LikeCommentView.as_view(), name="like_comment"),
    path("comments/<int:id>/", SpecificCommentView.as_view(),
         name="specific_comment"),
    # Notifications urls
    path('inbox/notifications/',
         include(notifications.urls, namespace='notifications')),
    path('notifications/', include(notifications_rest.urls)),
    path("my_notifications/", ListMyNotificationsView.as_view(),
         name="my_notifications"),
    path("my_notifications/<int:id>/", SpecificNotificationView.as_view(),
         name="specific_notification"),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

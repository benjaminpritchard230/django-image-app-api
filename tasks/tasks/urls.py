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
from django.urls import path
from todo.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'tasks'
urlpatterns = [
    path('admin/', admin.site.urls),
    # Api views
    path('tasks/', ListImagePosts.as_view(), name="tasks"),
    path('login/', obtain_auth_token, name="login"),
    path('posts/<int:id>/', SpecificImagePost.as_view(), name="specific_task"),
    path("register/", RegisterUserView.as_view(), name="register"),
]
# imp for what you want to achieve.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

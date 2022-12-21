from django.contrib import admin
from .models import ImagePost, Comment
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

# Register your models here.
admin.site.register(MyUser, UserAdmin)
admin.site.register(ImagePost)
admin.site.register(Comment)

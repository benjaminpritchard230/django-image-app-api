from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


class ImagePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="todolist", null=True)
    caption = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

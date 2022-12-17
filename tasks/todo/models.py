from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class ImagePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="todolist", null=True)
    caption = models.CharField(max_length=200)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    public = models.BooleanField(default=True, null=False)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="commenter", null=True)
    post = models.ForeignKey(
        ImagePost, on_delete=models.CASCADE, related_name="comments")
    # name = models.CharField(max_length=500, blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.ManyToManyField(
        User, blank=True, related_name="comment_likes")

    def __str__(self):
        return '%s-%s' % (self.post.caption, self.name)

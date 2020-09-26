from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='User')
    about = models.TextField(max_length=2000, null=True, blank=True, verbose_name='About')
    profile_pic = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Profile pic')

    def __str__(self):
        return self.user.username + "'s Profile"


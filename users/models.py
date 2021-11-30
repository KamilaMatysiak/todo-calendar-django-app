from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

AVATAR_DIMENSION = 400
THUMBNAIL_SIZE = (60, 60)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(null=True, max_length=200)
    birthdate = models.DateField(null=True)
    phonenumber = PhoneNumberField(null=False, blank=False, unique=True)

    avatar = models.ImageField('profile picture', upload_to='static/image/avatars/', null=True, blank=True)
    avatar_thumb = models.ImageField(upload_to="static/image/avatars/thumbs/", blank=True, null=True)
    __orig_avatar = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__orig_avatar = self.avatar

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__orig_avatar and not self.avatar and self.avatar_thumb:
            self.avatar_thumb = None
            self.__orig_avatar = None
            self.save()

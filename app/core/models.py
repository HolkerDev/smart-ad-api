import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


def advertising_image_file_path(instance, filename):
    """generate filepath for new advertising image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/advertising/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email: str, password=None, **args):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=self.normalize_email(email), **args)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password=None):
        """Creates and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"


class Audience(models.Model):
    """Model that represents advertising audience"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Device(models.Model):
    """Device object for advertising"""
    name = models.CharField(max_length=255)
    longitude = models.CharField(max_length=20, default='0.000000')
    latitude = models.CharField(max_length=20, default='0.000000')
    is_active = models.BooleanField(default=False)
    key = models.CharField(default='', max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Advertising(models.Model):
    """Advertising object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, upload_to=advertising_image_file_path)
    devices = models.ManyToManyField('Device')
    name = models.CharField(max_length=255, default='')
    audiences = models.ManyToManyField('Audience')
    fromDate = models.DateTimeField(auto_now_add=True, blank=True)
    toDate = models.DateTimeField(blank=True)
    seconds = models.IntegerField(default=0)

    def __str__(self):
        return self.name

from __future__ import unicode_literals
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse
from PIL import Image

# from touristalbum.album.templatetags.album_tags import user_name


class Lang(models.Model):
    lang_code = models.CharField(max_length=8)
    lang_name = models.CharField(max_length=32)

    def __str__(self):
        return self.lang_name


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return 'img/avatars/' + str(self.pk) + '/avatar.png'


def get_default_profile_image():
    return "img/avatars/default_avatar.png"


class AdvUser(AbstractBaseUser):
    username = models.CharField(max_length=30, verbose_name='Username')
    email = models.EmailField(unique=True, max_length=64, verbose_name='E-mail')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Last login time')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=24, blank=True, null=True)
    last_name = models.CharField(max_length=24, blank=True, null=True)
    send_messages = models.BooleanField(default=True, db_index=True)
    user_lang = models.ForeignKey('Lang', default='1', on_delete=models.SET_DEFAULT)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, blank=True)
    hide_email = models.BooleanField(default=True)
    email_verify = models.BooleanField(default=False)  # идентификация по email

    # используем идентификатор e-mail
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    # NOTE: shrink image on upload

    def save(self, *args, **kwargs):
        super().save()

        try:
            f_path = self.avatar.path
            ava = Image.open(f_path)

            if ava.height > 250 or ava.width > 250:
                output_size = (250, 250)
                ava.thumbnail(output_size)
                ava.save(self.avatar.path)
        except:
            print(u'не удалось открыть файл')


    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.pk})

    def get_profile_image_filename(self):
        return str(self.avatar)[str(self.avatar).index('img/avatars/' + str(self.pk) + "/"):]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def get_avatar_url(self):
        if self.avatar:
            avater_src = self.avatar.url
        else:
            avater_src = "/media/img/avatars/default_avatar.png"
        return avater_src

    def get_user_name(self):
        if self.first_name:
            user_name = self.first_name
            if self.last_name:
                user_name = user_name + ' ' + self.last_name

            user_name =  user_name + ' (' + self.username + ')'

        else:
            user_name = self.username
        return user_name
import os

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from languages.fields import RegionField, LanguageField


class LanveUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            date_of_birth=date_of_birth,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


#  upload_to path of a profile picture
def profile_pic_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post/<post_title>.拡張子
    filename_divided = os.path.splitext(filename)
    ext = filename_divided[1]
    filename = 'users/{0}{1}'.format(instance.username, ext)
    return filename


GENDER_CHOICES = (
    ('1', 'Male'),
    ('2', 'Female'),
    ('3', 'Custom')
)


class LanveUser(AbstractBaseUser):
    """
       LanveUser is only for Shunta's web app 'Lanve'

       An abstract base class implementing a fully featured User model with
       admin-compliant permissions.

       Username and password are required. Other fields are optional.
       """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
        blank=False,
    )
    first_name = models.CharField('first name', max_length=30, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=False,
    )
    date_of_birth = models.DateField()
    profile_pic = models.ImageField(
        verbose_name='profile pic',
        width_field=300,
        height_field=300,
        upload_to=profile_pic_directory_path,
        blank=False)
    gender = models.CharField(
        "gender",
        max_length=2,
        choices=GENDER_CHOICES,
        blank=False
    )
    nationality = RegionField(
        'nationality',
        blank=False
    )
    residence = RegionField(
        'residence',
        blank=False
    )
    mother_tongue = LanguageField(
        'mother tongue',
        max_length=8,
        blank=False
    )
    following = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    answer_num = models.IntegerField(
        verbose_name='the numbers of answer',
        default=0
    )
    helpful = models.IntegerField(
        verbose_name='the numbers of helpful',
        default=0
    )
    not_helpful = models.IntegerField(
        verbose_name='the numbers of not helpful',
        default=0
    )
    good = models.IntegerField(
        verbose_name='the numbers of good',
        default=0
    )
    bad = models.IntegerField(
        verbose_name='the numbers of bad',
        default=0
    )
    created_at = models.DateTimeField('Created at', default=timezone.now)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = LanveUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'date_of_birth',
        'gender',
        'nationality',
        'mother_tongue',
    ]

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



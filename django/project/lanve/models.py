import os

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from languages.fields import RegionField, LanguageField

from stdimage import StdImageField


class LanveUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None):
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
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#  upload_to path of a profile picture
def profile_pic_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post/<post_title>.ext
    filename_divided = os.path.splitext(filename)
    ext = filename_divided[1]
    filename = 'users/profile/{0}{1}'.format(instance.username, ext)
    return filename


# set a default user profile picture when an user make a new account
def get_default_profile_picture():
    path = 'users/profile/default-user-profile-picture.thumbnail.jpg'
    return path


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
        blank=True,
    )
    first_name = models.CharField('first name', max_length=30, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        verbose_name='birthday',
        blank=True,
        null=True,
    )
    profile_pic = StdImageField(
        upload_to=profile_pic_directory_path,
        verbose_name='profile picture',
        default=get_default_profile_picture,
        blank=True,
        variations={
            'thumbnail': (300, 300, True),
        },
        delete_orphans=True)
    gender = models.CharField(
        "gender",
        max_length=2,
        choices=GENDER_CHOICES,
        blank=True
    )
    nationality = RegionField(
        'nationality',
        blank=True
    )
    residence = RegionField(
        'residence',
        blank=True
    )
    mother_tongue = LanguageField(
        'mother tongue',
        max_length=8,
        blank=True
    )

    # auto_now_add はインスタンスの作成(DBにINSERT)する度に更新
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    # # auto_now=Trueの場合はモデルインスタンスを保存する度に現在の時間で更新
    updated_at = models.DateTimeField('update_at', auto_now=True)
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
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Relationship(models.Model):
    following = models.ForeignKey(
        LanveUser,
        related_name='follows',
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        LanveUser,
        related_name='followers',
        on_delete=models.CASCADE,
    )
    # auto_now_add はインスタンスの作成(DBにINSERT)する度に更新
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    # # auto_now=Trueの場合はモデルインスタンスを保存する度に現在の時間で更新
    updated_at = models.DateTimeField('update_at', auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'relationship'


def set_default_contributor_issue_deleted():
    contributor = 'Disappeared user'
    return contributor


def set_default_region_issue_deleted():
    region_contributor = 'unknown'
    return region_contributor


class Issue(models.Model):
    question = models.TextField(verbose_name='question sentence', blank=False)
    situation = models.TextField(verbose_name='situation', blank=True)
    contributor = models.ForeignKey(
        LanveUser,
        on_delete=models.SET(set_default_contributor_issue_deleted),
        related_name='contributor_issue',
    )
    language_to = LanguageField(
        'language you want to translate to',
        max_length=8,
        blank=True
    )
    count_view = models.PositiveIntegerField(
        'the number of this issue view',
        default=0
    )
    # auto_now_add はインスタンスの作成(DBにINSERT)する度に更新
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    # # auto_now=Trueの場合はモデルインスタンスを保存する度に現在の時間で更新
    updated_at = models.DateTimeField('update_at', auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question


class Comment(models.Model):
    issue = models.ForeignKey(
        'Issue',
        verbose_name='issue',
        on_delete=models.CASCADE,
        related_name='issue',
    )
    contributor = models.ForeignKey(
        'LanveUser',
        verbose_name='contributor',
        on_delete=models.CASCADE,
        related_name='contributor_comment',
    )
    text = models.TextField('comment')
    like = models.ManyToManyField('LanveUser', blank=True, related_name="likes")
    # auto_now_add はインスタンスの作成(DBにINSERT)する度に更新
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    # # auto_now=Trueの場合はモデルインスタンスを保存する度に現在の時間で更新
    updated_at = models.DateTimeField('update_at', auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:10]


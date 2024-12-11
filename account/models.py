from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, contact, password=None, password2=None):

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact=contact

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, contact, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            contact=contact
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

#  Custom User Model


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    contact = models.CharField(
        max_length=15, null=True, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):

        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



            
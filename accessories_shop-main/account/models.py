from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required")
        if not user_name:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verify", True)
        extra_fields.setdefault("user_type", "developer")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_verify") is not True:
            raise ValueError("Superuser must have is_verify=True.")

        return self.create_user(email, user_name, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ("visitor", "visitor"),
        ("developer", "developer"),
    )

    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100, unique=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default="visitor")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)

    objects = CustomManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name}'s Profile"

    def save(self, *args, **kwargs):
        self.username = self.user.email.split("@", maxsplit=1)[0]
        super().save(*args, **kwargs)


@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=MyUser)
def save_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()

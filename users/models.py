from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import  PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common.validators import validate_phone
from users import manager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        admin = "admin", _("Admin")
        stadium_owner = "stadium_owner", _("Stadium Owner")
        customer = "customer", _("Customer")

    class Language(models.TextChoices):
        uzbek = "uz", _("O'zbek")
        russian = "ru", _("Русский")
        english = "en", _("English")

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone"
    objects = manager.CustomUserManager()

    username = models.CharField(
        _("username"),
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone = models.CharField(
        _("phone number"),
        max_length=12,
        validators=[validate_phone],
        unique=True,
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )
    role = models.CharField(
        _("role"),
        choices=Role.choices,
        max_length=20,
        default=Role.customer,
    )
    language = models.CharField(
        _("Language"),
        choices=Language.choices,
        max_length=20,
        default=Language.uzbek,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    email = models.EmailField(_("email address"), blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        unique_together = (("phone", "role"),)

    def __str__(self):
        return self.phone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Note: username as a phone
        Create and save a user with the given phone_number, email, and password
        """
        phone = username
        if not phone:
            raise ValueError("The given phone must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", "admin")
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **kwargs):  # noqa
        return self._create_user(
            username=phone, password=password, email=email, **kwargs
        )

    def create_superuser(self, phone, email=None, password=None, **kwargs):  # noqa
        return super(CustomUserManager, self).create_superuser(
            phone, email, password, **kwargs
        )  # noqa

from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not phone:
            raise ValueError('The given phone must be set')
        # email = self.normalize_email(email)
        user = self.model(phone=phone,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        return self._create_user(phone, password, False, False, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        return self._create_user(phone, password, True, True, **extra_fields)

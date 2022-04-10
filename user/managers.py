from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('the email must be set')
        if not username:
            raise ValueError('the username must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', true)
        extra_fields.setdefault('is_superuser', true)
        extra_fields.setdefault('is_active', true)

        if extra_fields.get('is_staff') is not true:
            raise valueerror('superuser must have is_staff=true.')
        if extra_fields.get('is_superuser') is not true:
            raise valueerror('superuser must have is_superuser=true.')
        return self.create_user(username, email, first_name, last_name, password, **extra_fields)

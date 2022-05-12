from django.contrib.auth.base_user import BaseUserManager


# custom manager for user model
class CustomUserManager(BaseUserManager):
    # create_user will take all the inputs and will make
    # a new user entry in the table
    def create_user(self, username, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('the email must be set')
        if not username:
            raise ValueError('the username must be set')
        norm_email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=norm_email,
            first_name=first_name,
            last_name=last_name,
        )
        # django will automatically hash this password
        # before setting it in the table to ensure
        # better security standards
        user.set_password(password)
        user.save()
        return user

    # this isn't necessary but if you wish to make an admin
    # account you can include this
    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username='admin',
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

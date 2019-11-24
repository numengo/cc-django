from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import is_password_usable


class User(AbstractUser):
    # https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
    email = EmailField(_('email address'), unique=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def has_usable_password(self):
        return is_password_usable(self.password)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['']


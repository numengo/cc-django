from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    # https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
    #username = None
    #email = EmailField(_('email address'), unique=True)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

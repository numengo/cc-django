from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .forms import UserChangeForm, UserCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets
    list_display = ["email", "is_superuser"]
    search_fields = ["email"]

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class LBUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class LBUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = LBUserChangeForm
    add_form = LBUserCreationForm
    fieldsets = (
        ('User Profile', {'fields': ('first_name', 'last_name', 'email')}),
    )
    list_display = (
        'first_name', 'last_name', 'email', 'is_provider', 'is_superuser'
    )
    search_fields = ['first_name', 'last_name', 'email']

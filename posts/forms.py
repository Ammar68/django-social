from django.contrib.auth.models import User
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('last_login', 'password', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'date_joined')
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
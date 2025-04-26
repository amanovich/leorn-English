from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class TeacherLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("Аккаунт отключён", code='inactive')
        if user.role != 'teacher':
            raise ValidationError("Доступ разрешён только учителям", code='invalid_login')

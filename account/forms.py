from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class passwordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)



class changePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = '__all__'
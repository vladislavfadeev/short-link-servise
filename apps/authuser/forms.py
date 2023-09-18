# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model, authenticate
# from django import forms
# from apps.authuser.utils import send_email_verify

# User = get_user_model()


# class CustomAuthenticationForm(AuthenticationForm):
#     def clean(self):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")

#         if username is not None and password:
#             self.user_cache = authenticate(
#                 self.request, username=username, password=password
#             )
#             if not self.user_cache.verified:
#                 send_email_verify(self.request, self.user_cache)
#                 raise ValidationError(
#                     "Email is not verify. Chek your mail",
#                     code="invalid_login",
#                 )
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={"autocomplete": "email"}),
#     )

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("email",)

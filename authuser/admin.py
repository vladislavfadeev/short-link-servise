from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from authuser.forms import CustomUserCreationForm


User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    ordering = ("username", "email", "is_staff")
    list_display_links = ("username", "email")
    # list_editable = ('email_verify', )



admin.site.site_title = 'Админ панель clkr.su'
admin.site.site_header = 'Админ панель clkr.su'
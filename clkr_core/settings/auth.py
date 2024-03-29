import os

# Django base auth settings
AUTH_USER_MODEL = "authuser.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

DJANGO_SUPERUSER_USERNAME = os.environ["DJANGO_SUPERUSER_USERNAME"]
DJANGO_SUPERUSER_PASSWORD = os.environ["DJANGO_SUPERUSER_PASSWORD"]
DJANGO_SUPERUSER_EMAIL = os.environ["DJANGO_SUPERUSER_EMAIL"]


# AllAuth app settings
ACCOUNT_ADAPTER = "apps.authuser.adapter.CustomAccountAdapter"

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_PREVENT_ENUMERATION = False

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": os.environ["SOCIALACCOUNT_GITHUB_CLIENT_ID"],
            "secret": os.environ["SOCIALACCOUNT_GITHUB_SECRET"],
        },
        "SCOPE": [
            "user",
            "repo",
            "email",
            "read:org",
        ],
        "VERIFIED_EMAIL": os.environ["SOCIALACCOUNT_GITHUB_VERIFIED_EMAIL"]
    },
    "google": {
        "APP": {
            "client_id": os.environ["SOCIALACCOUNT_GOOGLE_CLIENT_ID"],
            "secret": os.environ["SOCIALACCOUNT_GOOGLE_SECRET"],
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "VERIFIED_EMAIL": os.environ["SOCIALACCOUNT_GOOGLE_VERIFIED_EMAIL"],
    },
}

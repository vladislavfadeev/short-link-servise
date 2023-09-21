import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))


def reduce_path(file_name, times):
    result = os.path.realpath(file_name)
    for _ in range(times):
        result = os.path.dirname(result)
    return result


ROOT_DIR = reduce_path(__file__, 4)
BASE_DIR = reduce_path(__file__, 3)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

#DEBUG = os.environ["DEBUG"]
DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
SESSION_COOKIE_AGE = 10**8

ROOT_URLCONF = "clkr_core.urls"

LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Local apps
    "apps.authuser",
    "apps.cutter",
    "apps.db_model",
    "apps.home",
    "apps.dashboard",
    "apps.api",
    "apps.utils",
    # Third party apps
    "django_filters",
    "django_user_agents",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third party middleware
    "django_user_agents.middleware.UserAgentMiddleware",
    # Local middleware
    "apps.home.middleware.SetRealRemoteAddrMiddleware",
    "apps.home.middleware.UserUniqueUUIDMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "clkr_core.wsgi.application"

LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_ALLOW_ASYNC_UNSAFE = os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"]

PROJECT_NAME = os.environ["PROJECT_NAME"]
DOMAIN_NAME = os.environ["DOMAIN_NAME"]

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-fallback")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-fallback")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.users",
    "apps.access",
    "apps.mock_business",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "apps.users.middleware.JWTAuthMiddleware",
]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "auth_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

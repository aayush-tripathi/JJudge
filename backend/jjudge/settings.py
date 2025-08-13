import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","corsheaders","channels","apps.accounts","apps.contests","channels_postgres",   
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "jjudge.urls"
WSGI_APPLICATION = None
ASGI_APPLICATION = "jjudge.asgi.application"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL required.")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PGDATABASE", ""),
        "USER": os.getenv("PGUSER", ""),
        "PASSWORD": os.getenv("PGPASSWORD", ""),
        "HOST": os.getenv("PGHOST", ""),
        "PORT": os.getenv("PGPORT", ""),
        "OPTIONS": {"options": f"-c search_path=public"},
    }
}
CHANNELS_BACKEND = os.getenv("CHANNELS_BACKEND", "inmemory").lower()
CHANNELS_DB_URL = os.getenv("CHANNELS_DB_URL") or os.getenv("DATABASE_URL")
if CHANNELS_BACKEND == "postgres" and CHANNELS_DB_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_postgres.core.PostgresChannelLayer",
            "CONFIG": {"dsn": CHANNELS_DB_URL},
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",)}
from datetime import timedelta
SIMPLE_JWT = { "ACCESS_TOKEN_LIFETIME": timedelta(hours=6), "REFRESH_TOKEN_LIFETIME": timedelta(days=7), "AUTH_HEADER_TYPES": ("Bearer",), }
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates","DIRS": [],"APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.debug","django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages",]},
}]
LANGUAGE_CODE = "en-us"; TIME_ZONE = "UTC"; USE_I18N = True; USE_TZ = True
JUDGE_TIME_LIMIT_MS = int(os.getenv("JUDGE_TIME_LIMIT_MS", "2000"))
JUDGE_MEMORY_LIMIT_MB = int(os.getenv("JUDGE_MEMORY_LIMIT_MB", "256"))
DOCKER_ENABLED = os.getenv("DOCKER_ENABLED", "false").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

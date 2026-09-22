"""
Django settings for my_shop project.

Configuration follows the standard deployment contract: everything
environment-specific is read from the environment (optionally via a
``.env`` file placed next to ``manage.py``). See ``.env.example``.
"""
from pathlib import Path

import environ
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR is the directory holding manage.py.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # Default local-development values; real deployments set these in .env
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
    SECRET_KEY=(str, "django-insecure-^muzt342(d0_ktu884@4xa#63q6pu9xb70*097xjjqnm1^1(4%"),
    POSTGRES_DB=(str, ""),
    POSTGRES_USER=(str, ""),
    POSTGRES_PASSWORD=(str, ""),
    POSTGRES_HOST=(str, "127.0.0.1"),
    POSTGRES_PORT=(str, "5432"),
    REDIS_URL=(str, ""),
    STATIC_ROOT=(str, str(BASE_DIR / "collected_static")),
    MEDIA_ROOT=(str, str(BASE_DIR / "media")),
)

# Load .env from the manage.py directory, when present.
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "request",
    "erp_framework",
    "sales",
    "expense",
    "general_reports",
    "purchase",
    "request_analytics",
    "crequest",
    "crispy_forms",
    "crispy_bootstrap4",
    "reversion",
    "tabular_permissions",
    "erp_framework.admin.jazzy_tabler_integration",
    "erp_framework.admin",
    # "erp_framework.activity",
    "erp_framework.reporting",
    "slick_reporting",
    "my_shop",
    "jazzy_tabler",
    "django.contrib.admin",  # comes at the end because the theme is replaced
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "my_shop.middleware.SetCorrectIPMiddleware",
    "request.middleware.RequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # crequest
    "crequest.middleware.CrequestMiddleware",
]

ROOT_URLCONF = "my_shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "my_shop.wsgi.application"

# Database: Postgres when POSTGRES_DB is set, sqlite for local dev otherwise.
if env("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Cache: Redis when REDIS_URL is set, local-memory otherwise.
REDIS_URL = env("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT")

MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Behind-proxy (Cloudflare / rambo) HTTPS settings
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host and host != "*"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

SLICK_REPORTING_FORM_MEDIA = {}

SLICK_REPORTING_DEFAULT_CHARTS_ENGINE = "highcharts"

# RA_ADMIN_INDEX_PAGE = "admin/custom_index.html"
# RA_ADMIN_INDEX_TITLE = "My Shop"
JAZZY_SETTINGS = {
    "site_title": "My Shop ERP",
    "site_header": "My Shop ERP System",
    "site_brand": "My Shop ERP System",
    "welcome_sign": "Welcome to Django ERP framework demo site. \n Use Username:`test` Password:`testuser123` to login",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
        "sales": "fas fa-shopping-cart",
        "sales.sale": "fas fa-shopping-cart",
        "sales.client": "fas fa-user-tie",
        "sales.product": "fas fa-box",
        "purchase": "fas fa-truck",
        "purchase.purchase": "fas fa-truck",
        "expense": "fas fa-money-bill-wave",
        "expense.expense": "fas fa-money-bill-wave",
        "expense.expensetransaction": "fas fa-receipt",
    },
    "changeform_format": "horizontal_tabs",
    # Links to put along the top menu
    "topmenu_links": [
        {
            "name": "Requests Dashboard",
            "url": "/requests-dashboard/",
            "new_window": False,
        },
        {
            "name": "Front end dashboard",
            "url": "/front-end-dashboard",
            "new_window": True,
        },
    ],
}

JAZZY_UI_TWEAKS = {
    "navbar": "light",
    "sidebar": "dark",
    "default_theme_mode": "light",
    "accent_color": "primary",
}

ERP_FRAMEWORK_SETTINGS = {
    "index_title": "My Shop dashboard",
    "index_template": "admin/custom_index.html",
    # "report_base_template": "request_analytics/base.html",
    # "admin_base_site_template": "request_analytics/base.html",
    "sites": {
        "requests-dashboard": {
            "admin_base_site_template": "request_analytics/base.html",
            "index_template": "request_analytics/index.html",
        }
    },
}

LOGIN_REDIRECT_URL = reverse_lazy("admin:index", current_app="erp_framework_admin")

REQUEST_BASE_URL = "https://my-shop.django-erp.com"

IPWARE_META_PRECEDENCE_ORDER = (
    "HTTP_CF_CONNECTING_IP",
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",  # client, proxy1, proxy2
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
)

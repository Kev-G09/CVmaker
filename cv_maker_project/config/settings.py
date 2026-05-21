from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    
    # Registramos formtools para que funcione el Wizard de la guía
    'formtools',
    
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # ¡Corregido el guion por el punto aquí abajo!
    'django.middleware.common.CommonMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default':{
        'ENGINE' : 'mssql',
        'NAME' : 'CVMakerDB',
        'HOST': 'localhost',
        'OPTIONS': {
            'driver' : 'ODBC Driver 17 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
    },
}

SECRET_KEY = 'django-insecure-dev-key'

DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = 'static/'
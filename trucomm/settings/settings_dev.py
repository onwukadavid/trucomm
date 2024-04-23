from .base import *
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))

project_dir = os.path.dirname(os.path.dirname(current_dir))

env_file_path = os.path.join(project_dir, '.env.dev')

load_dotenv(env_file_path)

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }  
    }
}

AUTH_USER_MODEL = 'users.User'
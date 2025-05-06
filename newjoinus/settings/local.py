from .base import *
import environ

# 환경 변수 설정
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))  # .env 파일 읽기

SECRET_KEY = env('DJANGO_SECRET')

# S3 접근 설정
AWS_S3_ACCESS_KEY_ID = env("DJANGO_AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = env("DJANGO_AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_STORAGE_BUCKET_NAME = env("DJANGO_AWS_S3_STORAGE_BUCKET_NAME")
AWS_S3_REGION = env("DJANGO_AWS_S3_REGION")
AWS_S3_POST_IMAGE_FOLDER_NAME = "tmp-posts/"

ALLOWED_HOSTS = ['*']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
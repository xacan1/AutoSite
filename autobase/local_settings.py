from pathlib import Path

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR / 'static'
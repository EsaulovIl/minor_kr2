import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education.settings')

application = get_wsgi_application()

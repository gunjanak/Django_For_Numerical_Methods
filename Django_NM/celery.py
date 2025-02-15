import os
from celery import Celery

# Set default Django settings module for 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_NM.settings")  # Change 'your_project' to your actual project name

app = Celery("your_project")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

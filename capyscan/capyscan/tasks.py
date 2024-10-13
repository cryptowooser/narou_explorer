from celery import shared_task
from django.core.management import call_command
from django.utils import timezone

@shared_task
def fetch_daily_rankings():
    date = timezone.now().strftime('%Y-%m-%d')
    call_command('fetch_daily_rankings', date)

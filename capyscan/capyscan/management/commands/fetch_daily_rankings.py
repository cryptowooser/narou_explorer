from django.core.management.base import BaseCommand
from django.utils import timezone
from capyscan.models import DailyRankings, NovelInfo
import requests
import json
from datetime import datetime, timedelta
import gzip

class Command(BaseCommand):
    help = 'Fetches top 30 daily stories from Syosetu API for a specific date and updates NovelInfo'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='Date in YYYY-MM-DD format')

    def handle(self, *args, **options):
        date = options['date']
        stories = self.get_top_30_daily_stories(date)
        if stories:
            self.save_stories_to_db(stories, date)
            self.update_novel_info(stories)
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched and saved {len(stories)} stories for {date} and updated NovelInfo'))
        else:
            self.stdout.write(self.style.WARNING(f'No stories fetched for {date}'))

    def get_top_30_daily_stories(self, date):
        url = "https://api.syosetu.com/novelapi/api/"

        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self.stderr.write(self.style.ERROR("Invalid date format. Please use YYYY-MM-DD."))
            return []

        next_day = target_date + timedelta(days=1)
        start_timestamp = int(target_date.timestamp())
        end_timestamp = int(next_day.timestamp()) - 1

        params = {
            "out": "json",
            "order": "dailypoint",
            "lim": 30,
            "of": "n-dp-t-w-s-bg-g-k-l",  # Added fields for NovelInfo update
            "lastup": f"{start_timestamp}-{end_timestamp}",
            "gzip": 5
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            decompressed_data = gzip.decompress(response.content)
            data = json.loads(decompressed_data.decode('utf-8'))
            return data[1:]  # Remove the first element (count) and return the stories
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'An error occurred while fetching data: {e}'))
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'An error occurred while parsing JSON: {e}'))
        except gzip.BadGzipFile as e:
            self.stderr.write(self.style.ERROR(f'An error occurred while decompressing gzip data: {e}'))
        return []

    def save_stories_to_db(self, stories, date):
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        for story in stories:
            DailyRankings.objects.update_or_create(
                ncode=story['ncode'],
                date=target_date,
                defaults={
                    'daily_points': story['daily_point'],
                }
            )

    def update_novel_info(self, stories):
        for story in stories:
            NovelInfo.objects.update_or_create(
                ncode=story['ncode'],
                defaults={
                    'title': story['title'],
                    'writer': story['writer'],
                    'story': story['story'],
                    'biggenre': story['biggenre'],
                    'genre': story['genre'],
                    'keyword': story['keyword'],
                    'length': story['length'],
                }
            )

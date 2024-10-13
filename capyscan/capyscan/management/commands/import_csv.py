import csv
from django.core.management.base import BaseCommand
from capyscan.models import NovelInfo

class Command(BaseCommand):
    help = 'Load a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                novel = NovelInfo(
                    title=row['title'],
                    ncode=row['ncode'],
                    writer=row['writer'],
                    story=row['story'],
                    biggenre=row['biggenre'],
                    genre=row['genre'],
                    keyword=row['keyword'],
                    length=row['length']
                )
                novel.save()

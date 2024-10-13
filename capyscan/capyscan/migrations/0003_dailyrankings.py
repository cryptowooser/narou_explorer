# Generated by Django 4.2.6 on 2024-10-13 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capyscan', '0002_userrowignore'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyRankings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ncode', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('daily_points', models.IntegerField()),
            ],
            options={
                'ordering': ['-date', '-daily_points'],
                'unique_together': {('ncode', 'date')},
            },
        ),
    ]

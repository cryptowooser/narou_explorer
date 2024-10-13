from django.db import models
from django.contrib.auth.models import User

class NovelInfo(models.Model):
    title = models.CharField(max_length=255)
    ncode = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    story = models.TextField()
    biggenre = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    keyword = models.TextField()
    length = models.PositiveIntegerField()

class UserRowIgnore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.ForeignKey(NovelInfo, on_delete=models.CASCADE)
    is_ignored = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'row')


class DailyRankings(models.Model):
    ncode = models.CharField(max_length=20)
    date = models.DateField()
    daily_points = models.IntegerField()

    class Meta:
        unique_together = ('ncode', 'date')
        ordering = ['-date', '-daily_points']

    def __str__(self):
        return f"{self.ncode} - {self.date} - {self.daily_points} points"
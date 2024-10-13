from django.shortcuts import render
from django.contrib.auth.models import User
from .models import NovelInfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import UserRowIgnore, DailyRankings
import logging
from django.db.models import Max, F, OuterRef, Subquery
from datetime import timedelta, datetime
from django.urls import reverse

logger = logging.getLogger(__name__)

BIGGENRE_CODES = {
    "1": "恋愛",
    "2": "ファンタジー",
    "3": "文芸",
    "4": "SF",
    "98": "ノンジャンル",
    "99": "その他",
    
}

GENRE_CODES = {
    "0": "未選択〔未選択〕",
    "101": "異世界〔恋愛〕",
    "102": "現実世界〔恋愛〕",
    "201": "ハイファンタジー〔ファンタジー〕",
    "202": "ローファンタジー〔ファンタジー〕",
    "301": "純文学〔文芸〕",
    "302": "ヒューマンドラマ〔文芸〕",
    "303": "歴史〔文芸〕",
    "304": "推理〔文芸〕",
    "305": "ホラー〔文芸〕",
    "306": "アクション〔文芸〕",
    "307": "コメディー〔文芸〕",
    "401": "VRゲーム〔SF〕",
    "402": "宇宙〔SF〕",
    "403": "空想科学〔SF〕",
    "404": "パニック〔SF〕",
    "9901": "童話〔その他〕",
    "9902": "詩〔その他〕",
    "9903": "エッセイ〔その他〕",
    "9904": "リプレイ〔その他〕",
    "9999": "その他〔その他〕",
    "9801": "ノンジャンル〔ノンジャンル〕"
}

@login_required
def index(request):
    user = request.user
    
    # Get the most recent date from DailyRankings
    latest_date = DailyRankings.objects.aggregate(Max('date'))['date__max']
    
    # Get the requested date from the query parameters, default to latest_date
    current_date = request.GET.get('date', latest_date)
    if current_date != latest_date:
        try:
            current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        except ValueError:
            current_date = latest_date
    
    # Calculate previous and next dates
    prev_date = DailyRankings.objects.filter(date__lt=current_date).aggregate(Max('date'))['date__max']
    next_date = DailyRankings.objects.filter(date__gt=current_date).order_by('date').first()
    next_date = next_date.date if next_date else None

    # Subquery to get daily_points
    daily_points_subquery = DailyRankings.objects.filter(
        ncode=OuterRef('ncode'),
        date=current_date
    ).values('daily_points')[:1]
    
    # Get novels from the current date, ordered by daily_points
    novels = NovelInfo.objects.filter(
        ncode__in=DailyRankings.objects.filter(date=current_date).values('ncode')
    ).annotate(
        daily_points=Subquery(daily_points_subquery)
    ).order_by('-daily_points')

    ignored_novel_ids = UserRowIgnore.objects.filter(user=user, is_ignored=True).values_list('row_id', flat=True)

    for novel in novels:
        novel.is_ignored = novel.id in ignored_novel_ids
        novel.biggenre_name = BIGGENRE_CODES.get(novel.biggenre, "Unknown")
        novel.genre_name = GENRE_CODES.get(novel.genre, "Unknown")

    context = {
        'user': user,
        'novels': novels,
        'current_date': current_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'latest_date': latest_date,
    }

    return render(request, 'index.html', context)

@login_required
@require_POST
def save_ignored_novels(request):
    logger.debug(f"POST Data: {request.POST}")
    ignored_novel_ids = request.POST.getlist('ignored_novels')
    logger.debug(f"Ignored Novel IDs: {ignored_novel_ids}")

    UserRowIgnore.objects.filter(user=request.user).delete()
    for novel_id in ignored_novel_ids:
        novel = NovelInfo.objects.get(id=novel_id)
        UserRowIgnore.objects.create(user=request.user, row=novel, is_ignored=True)

    # Get the current date from the form data
    current_date = request.POST.get('current_date')
    
    # Redirect back to the same page with the date parameter
    return redirect(f'{reverse("index")}?date={current_date}')

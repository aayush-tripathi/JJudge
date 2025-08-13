from django.urls import re_path
from apps.contests.consumers import LeaderboardConsumer

websocket_urlpatterns = [
    re_path(r"^ws/leaderboard/(?P<contest_id>\d+)/$", LeaderboardConsumer.as_asgi()),
]

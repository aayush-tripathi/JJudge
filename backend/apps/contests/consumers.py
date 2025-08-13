from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from apps.contests.models import Submission
from django.db.models import Max
@sync_to_async
def _rows(contest_id: int):
    agg = (Submission.objects
           .filter(problem__contest_id=contest_id)
           .values("user__username")
           .annotate(best_score=Max("score"), last_id=Max("id"))
           .order_by("-best_score", "last_id"))
    return [{"user": a["user__username"], "score": a["best_score"]} for a in agg]

class LeaderboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.contest_id = int(self.scope["url_route"]["kwargs"]["contest_id"])
        self.group = f"lb_{self.contest_id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
        await self.send_json({"type": "leaderboard", "data": await _rows(self.contest_id)})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def leaderboard_update(self, event):
        await self.send_json({"type": "leaderboard", "data": await _rows(self.contest_id)})

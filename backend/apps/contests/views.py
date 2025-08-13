
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contest, Problem, Submission
from .serializers import ContestSerializer, ProblemSerializer, SubmissionSerializer, SubmissionCreateSerializer
from .judge import run_submission
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
logger = logging.getLogger(__name__)  
class ContestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contest.objects.all().order_by("-start_time")
    serializer_class = ContestSerializer
    permission_classes = [permissions.AllowAny]
class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.AllowAny]
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().order_by("-created_at")
    serializer_class = SubmissionSerializer
    def get_permissions(self):
        if self.action in ["create","list","retrieve"]: return [permissions.IsAuthenticated()]
        return super().get_permissions()
    def get_serializer_class(self):
        return SubmissionCreateSerializer if self.action=="create" else SubmissionSerializer
    def perform_create(self, serializer): serializer.save(user=self.request.user, status="PENDING")
    def create(self, request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        s = self.get_serializer(data=request.data); s.is_valid(raise_exception=True)
        sub = Submission.objects.create(problem=s.validated_data["problem"], user=request.user, language=s.validated_data["language"], source=s.validated_data["source"], status="RUNNING")
        tcs = list(sub.problem.testcases.order_by("id").values_list("input_text","output_text"))
        result = run_submission(sub.language, sub.source, tcs)
        sub.status = result["status"]; sub.verdict_text = str(result["details"])[:5000]; sub.score = result["score"]; sub.save()
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
            f"lb_{sub.problem.contest_id}",
            {"type": "leaderboard.update", "contest_id": sub.problem.contest_id},
        )
        else:
            logger.warning("Channel layer is None; skipping leaderboard broadcast")
        return Response(SubmissionSerializer(sub).data, status=status.HTTP_201_CREATED)
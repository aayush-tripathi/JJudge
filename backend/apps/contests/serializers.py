from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contest, Problem, TestCase, Submission
User = get_user_model()
class TestCaseSerializer(serializers.ModelSerializer):
    class Meta: model = TestCase; fields = ("id","is_sample","input_text","output_text")
class ProblemSerializer(serializers.ModelSerializer):
    testcases = TestCaseSerializer(many=True, read_only=True)
    class Meta: model = Problem; fields = ("id","contest","title","slug","statement","time_limit_ms","memory_limit_mb","language_mask","testcases")
class ContestSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)
    class Meta: model = Contest; fields = ("id","name","start_time","end_time","problems")
class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta: model = Submission; fields = ("id","problem","user","language","source","status","verdict_text","score","created_at"); read_only_fields=("status","verdict_text","score","created_at")
class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta: model = Submission; fields = ("problem","language","source")
    def validate_language(self, value):
        if value not in ("py", "cpp", "js"):
            raise serializers.ValidationError("Unsupported language.")
        return value


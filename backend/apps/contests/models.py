from django.db import models
from django.conf import settings
class Contest(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self): return self.name
class Problem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="problems")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    statement = models.TextField()
    time_limit_ms = models.IntegerField(default=2000)
    memory_limit_mb = models.IntegerField(default=256)
    language_mask = models.CharField(max_length=64, default="py,cpp,js")
    def __str__(self): return f"{self.contest.name} — {self.title}"
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="testcases")
    input_text = models.TextField()
    output_text = models.TextField()
    is_sample = models.BooleanField(default=False)
class Submission(models.Model):
    STATUS_CHOICES = [("PENDING","PENDING"),("RUNNING","RUNNING"),("AC","AC"),("WA","WA"),("TLE","TLE"),("RE","RE"),("CE","CE"),("IE","IE")]
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    language = models.CharField(max_length=8)
    source = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="PENDING")
    verdict_text = models.TextField(blank=True, default="")
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

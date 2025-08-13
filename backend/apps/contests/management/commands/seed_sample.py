from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.contests.models import Contest, Problem, TestCase
from datetime import timedelta
class Command(BaseCommand):
    help = "Seed a sample contest and problem"
    def handle(self, *args, **kwargs):
        now = timezone.now()
        c, _ = Contest.objects.get_or_create(name="JJudge Sample", defaults={"start_time": now - timedelta(hours=1), "end_time": now + timedelta(days=1)})
        p, _ = Problem.objects.get_or_create(contest=c, slug="sum-two-numbers", defaults={"title":"Sum Two Numbers","statement":"Read two integers and print their sum.","time_limit_ms":2000,"memory_limit_mb":256,"language_mask":"py,cpp,js"})
        if not p.testcases.exists():
            TestCase.objects.create(problem=p, input_text="2 3\n", output_text="5\n", is_sample=True)
            TestCase.objects.create(problem=p, input_text="10 20\n", output_text="30\n", is_sample=False)
        self.stdout.write(self.style.SUCCESS("Seeded sample data."))

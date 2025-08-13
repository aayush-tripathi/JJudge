# apps/contests/admin.py
from django.contrib import admin
from .models import Contest, Problem, TestCase, Submission

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "contest", "testcases_count")
    search_fields = ("title",)
    list_filter = ("contest",)

    def testcases_count(self, obj):
        return obj.testcases.count()
    testcases_count.short_description = "Testcases"

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "problem")
    list_filter = ("problem",)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "problem", "user", "language", "status", "score", "created_at")
    list_filter = ("status", "language", "problem")
    search_fields = ("user__username",)

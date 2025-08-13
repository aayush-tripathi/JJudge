from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContestViewSet, ProblemViewSet, SubmissionViewSet
router = DefaultRouter()
router.register(r"contests", ContestViewSet, basename="contest")
router.register(r"problems", ProblemViewSet, basename="problem")
router.register(r"submissions", SubmissionViewSet, basename="submission")
urlpatterns = [ path("", include(router.urls)), ]

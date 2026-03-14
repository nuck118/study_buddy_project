from rest_framework import routers
from django.urls import path, include
from .views import (
    SubjectViewSet, MaterialViewSet, GoalViewSet, QuestionViewSet,
    JournalViewSet, ProfileView, PracticalViewSet, GoogleAuthView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'journal', JournalViewSet, basename='journal')
router.register(r'practical', PracticalViewSet, basename='practical')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='api-profile'),
    path('auth/google/', GoogleAuthView.as_view(), name='api-google-auth'),
]

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from ..models import Subject, Material, Goal, Question, Profile, UserProgress, JournalEntry, Certificate, PracticalChallenge
from .serializers import (
    SubjectSerializer, MaterialSerializer, GoalSerializer, QuestionSerializer,
    ProfileSerializer, JournalEntrySerializer, PracticalChallengeSerializer, UserSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
import requests


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class GoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class JournalViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user).order_by('-date', 'start_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return Response(ProfileSerializer(profile).data)

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PracticalChallenge.objects.all()
    serializer_class = PracticalChallengeSerializer


class GoogleAuthView(APIView):
    """Accepts a Google ID token from the client, verifies it with Google,
    creates or finds a Django user, and returns JWT tokens.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        id_token = request.data.get('id_token')
        if not id_token:
            return Response({'detail': 'Missing id_token'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify token with Google tokeninfo endpoint
        resp = requests.get('https://oauth2.googleapis.com/tokeninfo', params={'id_token': id_token})
        if resp.status_code != 200:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        data = resp.json()
        # data contains fields like 'email', 'email_verified', 'sub' (user id), 'name'
        email = data.get('email')
        if not email:
            return Response({'detail': 'Token did not contain email'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        if created:
            # Create profile
            Profile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

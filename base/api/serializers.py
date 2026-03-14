from rest_framework import serializers
from ..models import Subject, Material, Goal, Question, Profile, UserProgress, JournalEntry, Certificate, PracticalChallenge
from django.contrib.auth.models import User


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'subject', 'title', 'link', 'content_type']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'subject', 'description', 'points']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'goal', 'question_text', 'option_1', 'option_2', 'option_3', 'option_4']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'total_score', 'bio', 'profile_pic']


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'user', 'title', 'description', 'date', 'start_time', 'end_time', 'image', 'created_at']


class PracticalChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalChallenge
        fields = ['id', 'goal', 'instruction', 'starter_code', 'hint']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

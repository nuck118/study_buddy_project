from django.contrib import admin
from .models import Subject, Material, Goal, Profile, UserProgress, JournalEntry, Certificate, Question, PracticalChallenge

# 1. Setup Questions to appear inside the Goal page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

# 2. Setup Practical Challenges to appear inside the Goal page
class PracticalChallengeInline(admin.StackedInline):
    model = PracticalChallenge
    extra = 0

# 3. Connect them to the Goal Admin
class GoalAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, PracticalChallengeInline]

# 4. Register Everything
admin.site.register(Subject)
admin.site.register(Material)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Profile)
admin.site.register(UserProgress)
admin.site.register(JournalEntry)
admin.site.register(Certificate)
# admin.site.register(PracticalChallenge) # No need to register separately, it's inside Goal
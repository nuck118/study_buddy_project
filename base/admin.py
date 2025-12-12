from django.contrib import admin
from .models import Subject, Material, Goal, Profile, UserProgress, Question

# This allows us to add Questions directly inside the Goal page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class GoalAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Subject)
admin.site.register(Material)
admin.site.register(Goal, GoalAdmin) # <--- Update this line
admin.site.register(Profile)
admin.site.register(UserProgress)
# admin.site.register(Question) # No need to register separately if using Inline
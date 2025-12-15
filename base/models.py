from django.db import models
from django.contrib.auth.models import User
import re
import uuid 

# ... Keep Subject model as is ...

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Material(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.URLField() 
    content_type = models.CharField(max_length=50, choices=[
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('article', 'Article')
    ])

    def __str__(self): return self.title

    # NEW: Helper to convert YouTube links to Embed format
    def get_embed_url(self):
        # 1. Handle YouTube
        if "youtube.com" in self.link or "youtu.be" in self.link:
            # Regex to grab the 11-char ID
            import re
            regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
            match = re.search(regex, self.link)
            
            if match:
                video_id = match.group(1)
                # IMPORTANT: We add '?rel=0' (no recommended videos) and 'origin' (fixes localhost error)
                return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&origin=http://127.0.0.1:8000"
        
        # 2. Handle Google Drive / Docs (for PDFs)
        if "drive.google.com" in self.link and "/view" in self.link:
            return self.link.replace("/view", "/preview")
            
        return self.link
    

class Goal(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    points = models.IntegerField(default=10)

    def __str__(self): return self.description

# NEW: Quiz Question Model
class Question(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    
    # Store the correct answer as '1', '2', '3', or '4'
    correct_option = models.CharField(max_length=1, choices=[
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
    ])

    def __str__(self): return self.question_text

# ... Keep Profile and UserProgress as is ...
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    
    # NEW FIELDS
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pics/")

    def __str__(self):
        return self.user.username

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('user', 'goal')
    def __str__(self): return f"{self.user.username} - {self.goal.description}"
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    
    # NEW FIELDS
    start_time = models.TimeField() 
    end_time = models.TimeField()
    
    image = models.ImageField(upload_to='journal_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date})"
class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return f"Certificate: {self.user.username} - {self.subject.name}"
class PracticalChallenge(models.Model):
    goal = models.OneToOneField(Goal, on_delete=models.CASCADE) # One challenge per goal
    instruction = models.TextField() # e.g., "Create an h1 tag with 'Hello'"
    starter_code = models.TextField(default="<h1></h1>") # Initial code in the box
    hint = models.TextField(blank=True)
    
    # Validation: We will check if the user's code contains this string
    validation_text = models.CharField(max_length=100) # e.g., "color: blue"
    
    def __str__(self):
        return f"Challenge: {self.goal.description}"
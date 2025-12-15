from django.shortcuts import render
from .models import Subject, Material, Goal, Profile, UserProgress
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages # Import for error messages
from .models import Subject, Material, Goal, Question, Profile, UserProgress, JournalEntry
from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificate
from .utils import generate_certificate_image
from django.utils import timezone
from .models import PracticalChallenge 


def check_course_completion(user, subject):
    # Get total goals for this subject
    total_goals = Goal.objects.filter(subject=subject).count()
    
    # Get completed goals for this user & subject
    completed_goals = UserProgress.objects.filter(user=user, goal__subject=subject, is_completed=True).count()

    if total_goals > 0 and completed_goals == total_goals:
        # Check if certificate already exists
        if not Certificate.objects.filter(user=user, subject=subject).exists():
            # GENERATE CERTIFICATE
            img_file = generate_certificate_image(
                user.username, 
                subject.name, 
                timezone.now().strftime("%Y-%m-%d")
            )
            cert = Certificate.objects.create(user=user, subject=subject)
            cert.image.save(f"cert_{user.id}_{subject.id}.png", img_file)
            return cert
    return None
def home(request):
    # 1. CHECK: If user is NOT logged in, show the Landing Page
    if not request.user.is_authenticated:
        return render(request, 'base/landing.html')

    # 2. IF LOGGED IN: Run the Dashboard Logic
    subjects = Subject.objects.all()
    
    # Fetch Leaderboard
    leaderboard = Profile.objects.order_by('-total_score')[:5] 

    context = {'subjects': subjects, 'leaderboard': leaderboard}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def subject_page(request, pk):
    # 1. Fetch Subject
    subject = get_object_or_404(Subject, id=pk)
    
    # 2. Fetch Materials & Goals
    materials = subject.material_set.all()
    goals = subject.goal_set.all()

    # 3. Get Completed Goal IDs (to check off items)
    completed_ids = UserProgress.objects.filter(
        user=request.user, 
        is_completed=True
    ).values_list('goal_id', flat=True)

    context = {
        'subject': subject, 
        'materials': materials, 
        'goals': goals,
        'completed_ids': completed_ids 
        # Note: We do NOT need to pass 'challenges' here. 
        # The template accesses them via goal.practicalchallenge
    }
    return render(request, 'base/subject.html', context)
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    context = {'form': form, 'title': 'Login'}
    return render(request, 'base/login_register.html', context)

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Profile for the new user so they have a Score of 0
            Profile.objects.create(user=user) 
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    context = {'form': form, 'title': 'Register'}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
@login_required(login_url='login')
def mark_complete(request, subject_id, goal_id):
    if request.method == 'POST':
        goal = Goal.objects.get(id=goal_id)
        
        # Check if already completed
        already_done = UserProgress.objects.filter(user=request.user, goal=goal).exists()
        
        if not already_done:
            UserProgress.objects.create(user=request.user, goal=goal, is_completed=True)
            
            # --- FIX: Safe Profile Access ---
            # This gets the profile if it exists, OR creates it if it's missing
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            profile.total_score += goal.points
            profile.save()

            new_cert = check_course_completion(request.user, goal.subject)
        if new_cert:
            return redirect('certificate', pk=new_cert.id)
            
    return redirect('subject', pk=subject_id)
@login_required(login_url='login')
def submit_quiz(request, subject_id, goal_id):
    if request.method == 'POST':
        # 1. Fetch Goal and Questions
        goal = Goal.objects.get(id=goal_id)
        questions = goal.questions.all()
        
        score = 0
        total = questions.count()
        
        # 2. Grade the Quiz
        for q in questions:
            # Get user's selected option from the HTML form
            user_answer = request.POST.get(f'question_{q.id}')
            if user_answer == q.correct_option:
                score += 1
        
        # 3. Check Logic (Must get 100% to pass)
        if score == total:
            # Check if already completed to prevent double XP
            progress_exists = UserProgress.objects.filter(user=request.user, goal=goal).exists()
            
            if not progress_exists:
                # A. Mark as Done
                UserProgress.objects.create(user=request.user, goal=goal, is_completed=True)
                
                # B. Add XP (Safe Profile Access)
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.total_score += goal.points
                profile.save()
                
                messages.success(request, f"Quiz Passed! +{goal.points} XP")
                
                # C. Check for Certificate (Course Completion)
                new_cert = check_course_completion(request.user, goal.subject)
                if new_cert:
                    # Redirect to the celebration page
                    return redirect('certificate', pk=new_cert.id)
            else:
                messages.info(request, "You have already completed this quiz.")
        else:
            messages.error(request, f"You scored {score}/{total}. You need 100% to pass. Try again!")
            
    # If not a certificate redirect, go back to the subject page
    return redirect('subject', pk=subject_id)
@login_required(login_url='login')
def journal_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        # NEW INPUTS
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        image = request.FILES.get('image')

        JournalEntry.objects.create(
            user=request.user,
            title=title,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            image=image
        )
        return redirect('journal')

    # Sort by date, then by start_time
    entries = JournalEntry.objects.filter(user=request.user).order_by('-date', 'start_time')
    context = {'entries': entries}
    return render(request, 'base/journal.html', context)
@login_required(login_url='login')
def edit_journal(request, pk):
    entry = get_object_or_404(JournalEntry, id=pk, user=request.user)

    if request.method == 'POST':
        entry.title = request.POST.get('title')
        entry.date = request.POST.get('date')
        # UPDATE NEW FIELDS
        entry.start_time = request.POST.get('start_time')
        entry.end_time = request.POST.get('end_time')
        entry.description = request.POST.get('description')
        
        if request.FILES.get('image'):
            entry.image = request.FILES.get('image')
            
        entry.save()
        return redirect('journal')

    context = {'entry': entry}
    return render(request, 'base/journal_edit.html', context)
@login_required(login_url='login')
def profile_page(request):
    user = request.user
    
    # --- FIX: Safe Access ---
    # This gets the profile if it exists, OR creates it immediately if missing
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # 1. Update User Data (Auth)
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        # 2. Update Profile Data (Bio/Pic)
        profile.bio = request.POST.get('bio')
        
        # Check if a new image was uploaded
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')
        
        profile.save()
        return redirect('profile')

    context = {'user': user, 'profile': profile}
    return render(request, 'base/profile.html', context)
@login_required(login_url='login')
def certificate_view(request, pk):
    cert = get_object_or_404(Certificate, id=pk)
    context = {'cert': cert}
    return render(request, 'base/certificate.html', context)
@login_required(login_url='login')
def practical_page(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    # Get the challenge linked to this goal (or 404 if none exists)
    challenge = get_object_or_404(PracticalChallenge, goal=goal)
    
    context = {'goal': goal, 'challenge': challenge}
    return render(request, 'base/practical_lab.html', context)

@login_required(login_url='login')
def verify_code(request, challenge_id):
    if request.method == 'POST':
        challenge = get_object_or_404(PracticalChallenge, id=challenge_id)
        user_code = request.POST.get('code_submission')
        
        # Simple Validation: Check if the required text exists in their code
        # (In a real app, you'd parse the AST, but this works for basic learning)
        if challenge.validation_text.lower() in user_code.lower():
            
            # 1. Mark Goal Complete
            UserProgress.objects.get_or_create(
                user=request.user, 
                goal=challenge.goal, 
                defaults={'is_completed': True}
            )
            
            # 2. Award XP
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.total_score += challenge.goal.points
            profile.save()
            
            messages.success(request, f"Correct! +{challenge.goal.points} XP")
            return redirect('subject', pk=challenge.goal.subject.id)
        else:
            messages.error(request, "Not quite. Check the hint!")
            
    return redirect('practical', goal_id=challenge.goal.id)
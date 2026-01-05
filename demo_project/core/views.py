from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, GoalForm, StepForm, DailyStatusForm
from .models import Goal, TaskStep, DailyStatus, ActionLog
from .engine import next_step_for_user, apply_result, today_status, goal_score, get_user_achievements, get_user_level, get_motivation_message, get_goal_progress, get_weekly_stats
from django.utils import timezone
from datetime import timedelta
from collections import Counter

def signup_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            user = f.save()
            login(request, user)
            return redirect('dashboard')
    else:
        f = SignUpForm()
    return render(request, 'core/signup.html', {'form':f})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    # Try our primary template, fall back to the registration/login template if missing
    from django.template import TemplateDoesNotExist
    try:
        return render(request, 'core/login.html')
    except TemplateDoesNotExist:
        # In some deployments templates under 'core/' were not packaged — use a fallback
        messages.warning(request, "Using fallback login template")
        return render(request, 'registration/login.html')

def logout_view(request):
    logout(request); return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    profile = user.userprofile
    step = next_step_for_user(user)
    status = today_status(user)
    
    # User level and achievements
    level_info = get_user_level(profile.xp)
    achievements = get_user_achievements(user)
    motivation_msg = get_motivation_message(profile, status.energy, goal_score(Goal.objects.filter(user=user).first() or None) if Goal.objects.filter(user=user).exists() else 0)
    
    # Goal progress tracking
    goals = Goal.objects.filter(user=user)
    goal_data = []
    for g in goals:
        progress = get_goal_progress(g)
        score = goal_score(g)
        goal_data.append({'goal': g, 'progress': progress, 'score': score})
    
    # Gamification story
    total = ActionLog.objects.filter(user=user).count()
    fails = ActionLog.objects.filter(user=user, status='failed').count()
    fr = (fails/total) if total > 0 else 0
    
    if profile.streak >= 7: era='Legend Era'
    elif profile.streak >= 5: era='Consistency Era'
    elif profile.streak >= 2: era='Momentum Phase'
    else: era='Restart Arc'
    
    boss = 'Procrastination' if fr > 0.5 else ('Distraction' if fr > 0.2 else 'Self-Doubt')
    story = f"You are in the {era} 🎮 Boss: {boss}"
    
    return render(request, 'core/dashboard.html', {
        'next_step': step,
        'status': status,
        'story': story,
        'goals': goal_data,
        'level': level_info,
        'achievements': achievements,
        'motivation_msg': motivation_msg,
    })

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request,'core/goal_list.html', {'goals':goals})

@login_required
def goal_create(request):
    if request.method=='POST':
        f = GoalForm(request.POST)
        if f.is_valid():
            g = f.save(commit=False); g.user=request.user; g.save(); return redirect('goal_list')
    else: f = GoalForm()
    return render(request,'core/goal_form.html', {'form':f})

@login_required
def goal_detail(request, pk):
    g = get_object_or_404(Goal, pk=pk, user=request.user)
    steps_qs = g.steps.order_by('order')
    total = steps_qs.count()
    completed = steps_qs.filter(is_completed=True).count()
    progress_percent = int((completed / total) * 100) if total > 0 else 0
    return render(request,'core/goal_detail.html', {
        'goal': g,
        'steps': steps_qs,
        'total': total,
        'completed': completed,
        'progress_percent': progress_percent,
    })

@login_required
def add_step(request, goal_pk):
    g = get_object_or_404(Goal, pk=goal_pk, user=request.user)
    if request.method=='POST':
        f = StepForm(request.POST)
        if f.is_valid():
            s = f.save(commit=False); s.goal=g; s.save(); return redirect('goal_detail', pk=goal_pk)
    else: f = StepForm()
    return render(request,'core/step_form.html', {'form':f, 'goal':g})

@login_required
def do_step(request, step_pk, action):
    s = get_object_or_404(TaskStep, pk=step_pk, goal__user=request.user)
    if action in ('completed','failed','skipped'):
        apply_result(request.user, s, action)
    return redirect('dashboard')

@login_required
def daily_status(request):
    status = today_status(request.user)
    if request.method=='POST':
        f = DailyStatusForm(request.POST, instance=status)
        if f.is_valid(): f.save(); return redirect('dashboard')
    else:
        f = DailyStatusForm(instance=status)
    return render(request,'core/daily_status.html', {'form':f})

@login_required
def weekly_review(request):
    stats = get_weekly_stats(request.user)
    return render(request, 'core/weekly_review.html', {'stats': stats})

@login_required
def profile(request):
    prof = request.user.userprofile
    achievements = get_user_achievements(request.user)
    level_info = get_user_level(prof.xp)
    
    if request.method == 'POST':
        m = request.POST.get('motivation_mode')
        if m:
            prof.motivation_mode = m
            prof.save()
        return redirect('profile')
    
    return render(request, 'core/profile.html', {
        'profile': prof,
        'achievements': achievements,
        'level': level_info,
    })

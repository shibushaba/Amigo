from django.utils import timezone
from datetime import timedelta
from .models import Goal, TaskStep, DailyStatus, ActionLog
from django.db.models import Count, Q

def today_status(user):
    today = timezone.now().date()
    status, _ = DailyStatus.objects.get_or_create(user=user, date=today)
    return status

def get_goal_progress(goal):
    """Calculate real progress based on completed steps"""
    steps = goal.steps.all()
    total = max(1, steps.count())
    completed = steps.filter(is_completed=True).count()
    return int((completed / total) * 100)

def goal_score(goal):
    """Calculate goal health score based on multiple factors"""
    steps = goal.steps.all()
    total = max(1, steps.count())
    done = steps.filter(is_completed=True).count()
    
    # Real progress ratio (0-50 points)
    progress_ratio = done / total
    progress_score = int(50 * progress_ratio)
    
    # Recency bonus (0-20 points) - recent activity is better
    recent_7days = ActionLog.objects.filter(
        step__goal=goal, 
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).count()
    recency_score = min(recent_7days * 2, 20)
    
    # Consistency bonus (0-15 points) - steady progress
    this_week = ActionLog.objects.filter(
        step__goal=goal,
        status='completed',
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).count()
    consistency_score = min(this_week * 3, 15)
    
    # Failure penalty (-0 to -15 points)
    fails = ActionLog.objects.filter(step__goal=goal, status='failed').count()
    failure_penalty = min(fails * 3, 15)
    
    # Total score
    score = progress_score + recency_score + consistency_score - failure_penalty + 10
    return max(0, min(100, score))

def get_user_achievements(user):
    """Get list of user achievements/badges"""
    profile = user.userprofile
    achievements = []
    
    if profile.streak >= 7:
        achievements.append({'icon': '🔥', 'name': 'Week Warrior', 'desc': f'{profile.streak} day streak'})
    if profile.streak >= 30:
        achievements.append({'icon': '⭐', 'name': 'Month Master', 'desc': f'{profile.streak} day streak'})
    if profile.xp >= 500:
        achievements.append({'icon': '💎', 'name': 'XP Elite', 'desc': f'{profile.xp} XP earned'})
    if profile.xp >= 1000:
        achievements.append({'icon': '👑', 'name': 'Legend', 'desc': f'{profile.xp} XP earned'})
    
    # Goal completion achievements
    completed_goals = Goal.objects.filter(user=user, status='completed').count()
    if completed_goals >= 1:
        achievements.append({'icon': '✅', 'name': 'Goal Crusher', 'desc': f'{completed_goals} goal(s) completed'})
    if completed_goals >= 5:
        achievements.append({'icon': '🚀', 'name': 'Achiever', 'desc': f'{completed_goals} goals completed'})
    
    return achievements

def get_user_level(xp):
    """Calculate user level based on XP"""
    level = 1 + (xp // 200)
    next_level_xp = (level + 1) * 200
    current_level_xp = level * 200
    progress = ((xp - current_level_xp) / (next_level_xp - current_level_xp)) * 100
    return {'level': level, 'xp': xp, 'progress': int(progress)}

def get_motivation_message(profile, energy, goal_score_val):
    """Get personalized motivation message"""
    messages = {
        'soft': [
            'You\'re doing great! Take it easy. 💙',
            'One step at a time. You\'ve got this! 🌱',
            'Progress, not perfection! 🌟',
        ],
        'balanced': [
            'Keep pushing! You\'re on fire! 🔥',
            'Momentum is building! 💪',
            'Great pace! Let\'s keep going! ⚡',
        ],
        'hardcore': [
            'No excuses! Push harder! 💥',
            'You\'re a machine! Keep crushing! 🤖',
            'Legend status incoming! 👑',
        ],
        'reward': [
            f'You\'re earning {10} XP per step! 💰',
            'Every step counts! 🎁',
            f'You have {profile.coins} coins! Spend wisely! 💎',
        ]
    }
    mode = profile.motivation_mode
    import random
    return random.choice(messages.get(mode, messages['balanced']))

def next_step_for_user(user):
    """Get next recommended step based on goals, energy, and motivation"""
    profile = user.userprofile
    status = today_status(user)
    goals = Goal.objects.filter(user=user, active=True)
    
    if not goals.exists():
        return None
    
    # Prefer goals with better health scores
    scored = sorted([(goal_score(g), g) for g in goals], key=lambda x: -x[0])
    
    # Set difficulty bounds based on motivation mode and energy
    min_d, max_d = 1, 5
    
    if profile.motivation_mode == 'soft':
        max_d = 2 if status.energy < 40 else (3 if status.energy < 60 else 4)
    elif profile.motivation_mode == 'hardcore':
        min_d = 3 if status.energy > 50 else 2
    elif profile.motivation_mode == 'reward':
        # Mix of difficulties for engagement
        min_d = 1
        max_d = 4
    
    # Try to find step matching energy/motivation level
    for _, g in scored:
        step = g.steps.filter(
            is_completed=False,
            difficulty__gte=min_d,
            difficulty__lte=max_d
        ).order_by('order').first()
        if step:
            return step
    
    # Fallback: any incomplete step
    for _, g in scored:
        step = g.steps.filter(is_completed=False).order_by('order').first()
        if step:
            return step
    
    return None

def apply_result(user, step, result):
    """Apply action result and update user stats"""
    profile = user.userprofile
    today = timezone.now().date()
    
    if result == 'completed':
        step.is_completed = True
        step.completed_at = timezone.now()
        step.save()
        
        # Dynamic XP based on difficulty
        xp_reward = (step.difficulty * 5) + 10  # Level 1: 15, Level 5: 35
        profile.xp += xp_reward
        profile.coins += step.difficulty  # 1-5 coins
        
        # Streak logic - continuous daily engagement
        if profile.last_active:
            if profile.last_active == today - timedelta(days=1):
                profile.streak += 1
            elif profile.last_active != today:
                profile.streak = 1
        else:
            profile.streak = 1
        
        profile.last_active = today
        
        # Check if goal is complete
        goal = step.goal
        if goal.steps.filter(is_completed=False).count() == 0:
            goal.status = 'completed'
            goal.completed_at = timezone.now()
            goal.save()
            # Bonus for completing entire goal
            profile.xp += 50
            profile.coins += 10
        
    elif result == 'failed':
        step.fail_count += 1
        step.save()
        
        # Penalty based on motivation mode
        if profile.motivation_mode == 'hardcore':
            profile.xp = max(0, profile.xp - 10)
            if profile.streak > 0:
                profile.streak = max(0, profile.streak - 1)
        elif profile.motivation_mode == 'soft':
            # Minimal penalty for soft mode
            pass
        else:
            profile.xp = max(0, profile.xp - 3)
    
    elif result == 'skipped':
        # Skipping is neutral - no reward, no major penalty
        pass
    
    # Log the action
    ActionLog.objects.create(user=user, step=step, status=result)
    profile.save()

def get_weekly_stats(user):
    """Get comprehensive weekly statistics"""
    week_ago = timezone.now() - timedelta(days=7)
    
    total_actions = ActionLog.objects.filter(user=user, timestamp__gte=week_ago).count()
    completed = ActionLog.objects.filter(user=user, timestamp__gte=week_ago, status='completed').count()
    failed = ActionLog.objects.filter(user=user, timestamp__gte=week_ago, status='failed').count()
    skipped = ActionLog.objects.filter(user=user, timestamp__gte=week_ago, status='skipped').count()
    
    success_rate = int((completed / total_actions * 100)) if total_actions > 0 else 0
    
    # Most difficult step completed
    hardest = ActionLog.objects.filter(
        user=user,
        timestamp__gte=week_ago,
        status='completed'
    ).order_by('-step__difficulty').first()
    
    # Easiest step
    easiest = ActionLog.objects.filter(
        user=user,
        timestamp__gte=week_ago,
        status='completed'
    ).order_by('step__difficulty').first()
    
    # Most active goal
    from django.db.models import Count
    active_goal = ActionLog.objects.filter(
        user=user,
        timestamp__gte=week_ago
    ).values('step__goal').annotate(count=Count('id')).order_by('-count').first()
    
    return {
        'total': total_actions,
        'completed': completed,
        'failed': failed,
        'skipped': skipped,
        'success_rate': success_rate,
        'hardest': hardest.step if hardest else None,
        'easiest': easiest.step if easiest else None,
        'active_goal': active_goal,
    }

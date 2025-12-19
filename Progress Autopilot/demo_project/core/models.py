from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    MODES = [('soft','Soft'),('balanced','Balanced'),('hardcore','Hardcore'),('reward','Reward')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    motivation_mode = models.CharField(max_length=16, choices=MODES, default='balanced')
    xp = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self): return f"{self.user.username} profile"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    difficulty = models.IntegerField(default=3)
    created = models.DateTimeField(auto_now_add=True)
    # track goal lifecycle
    STATUS_CHOICES = [('active', 'Active'), ('completed', 'Completed')]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='active')
    completed_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class TaskStep(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=140)
    difficulty = models.IntegerField(default=3)
    order = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    fail_count = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f"{self.goal.title} → {self.title}"

class DailyStatus(models.Model):
    MOODS = [(1,'😔'),(2,'😐'),(3,'🙂'),(4,'😀'),(5,'🤩')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    energy = models.IntegerField(default=50)
    mood = models.IntegerField(choices=MOODS, default=3)
    notes = models.TextField(blank=True)
    class Meta:
        unique_together = ('user','date')

class ActionLog(models.Model):
    CHOICES=[('completed','Completed'),('failed','Failed'),('skipped','Skipped')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.ForeignKey(TaskStep, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

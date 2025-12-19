from django.contrib import admin
from .models import UserProfile, Goal, TaskStep, DailyStatus, ActionLog

admin.site.register(UserProfile)
admin.site.register(Goal)
admin.site.register(TaskStep)
admin.site.register(DailyStatus)
admin.site.register(ActionLog)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Goal, TaskStep, DailyStatus

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title','description','difficulty')

class StepForm(forms.ModelForm):
    class Meta:
        model = TaskStep
        fields = ('title','difficulty','order')

class DailyStatusForm(forms.ModelForm):
    class Meta:
        model = DailyStatus
        fields = ('energy','mood','notes')

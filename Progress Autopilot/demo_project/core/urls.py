from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('goals/', views.goal_list, name='goal_list'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/', views.goal_detail, name='goal_detail'),
    path('goals/<int:goal_pk>/add-step/', views.add_step, name='add_step'),

    path('step/<int:step_pk>/<str:action>/', views.do_step, name='do_step'),

    path('daily-status/', views.daily_status, name='daily_status'),
    path('weekly/', views.weekly_review, name='weekly_review'),
    path('profile/', views.profile, name='profile'),
]

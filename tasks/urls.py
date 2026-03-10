from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.get_tasks, name='get_tasks'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/questions/', views.add_question, name='add_question'),
    path('questions/<int:question_id>/', views.manage_question, name='manage_question'),
]

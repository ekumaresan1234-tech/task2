from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('ajax/create/', views.ajax_create_task, name='ajax-create'),
    path('ajax/update/<int:pk>/', views.ajax_update_task, name='ajax-update'),
    path('ajax/delete/<int:pk>/', views.ajax_delete_task, name='ajax-delete'),
    path('test-delete/<int:pk>/', views.test_delete, name='test-delete'),
]


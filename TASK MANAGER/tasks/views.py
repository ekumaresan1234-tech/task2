from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter task title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical',
                'rows': 4,
                'placeholder': 'Enter task description...'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            })
        }

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list_new.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task-list')

@csrf_exempt
@require_http_methods(["POST"])
def ajax_create_task(request):
    try:
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'pending')
        
        if not title or not title.strip():
            return JsonResponse({'success': False, 'error': 'Title is required'})
        
        task = Task.objects.create(
            title=title.strip(),
            description=description.strip(),
            status=status
        )
        return JsonResponse({
            'success': True,
            'id': task.id,
            'title': task.title,
            'status': task.get_status_display(),
            'created_at': task.created_at.isoformat()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def ajax_update_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        status = request.POST.get('status', task.status)
        
        if not title or not title.strip():
            return JsonResponse({'success': False, 'error': 'Title is required'})
        
        task.title = title.strip()
        task.description = description.strip()
        task.status = status
        task.save()
        
        return JsonResponse({
            'success': True,
            'id': task.id,
            'title': task.title,
            'status': task.get_status_display()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def ajax_delete_task(request, pk):
    try:
        print(f"Delete request received for task ID: {pk}")
        print(f"Request method: {request.method}")
        print(f"Request data: {request.POST}")
        
        task = get_object_or_404(Task, pk=pk)
        print(f"Task found: {task.title}")
        
        task.delete()
        print(f"Task deleted successfully")
        
        # Verify deletion
        exists = Task.objects.filter(id=pk).exists()
        print(f"Task exists after deletion: {exists}")
        
        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error in delete: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

def test_delete(request, pk):
    """Simple test delete function"""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return JsonResponse({'success': True, 'message': f'Task {pk} deleted'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


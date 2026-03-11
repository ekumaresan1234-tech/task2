from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'tasks/index.html', {'tasks': tasks, 'form': form})


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'tasks/update.html', {'form': form})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')


from django.shortcuts import render
from .models import Task

def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})
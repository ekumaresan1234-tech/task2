import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Task, Question

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all().order_by('-created_date')
        return JsonResponse([task.to_dict() for task in tasks], safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description', '')
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
            
        new_task = Task.objects.create(title=title, description=description)
        return JsonResponse(new_task.to_dict(), status=201)

@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
        
    if request.method == 'PUT':
        data = json.loads(request.body)
        status = data.get('status')
        
        if not status or status not in ['pending', 'completed']:
            return JsonResponse({'error': 'Invalid status'}, status=400)
            
        task.status = status
        task.save()
        return JsonResponse(task.to_dict())
        
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'success': True})

@csrf_exempt
def add_question(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
        
    if task.questions.count() >= 5:
        return JsonResponse({'error': 'A task cannot have more than 5 questions'}, status=400)
        
    data = json.loads(request.body)
    text = data.get('text')
    
    if not text:
        return JsonResponse({'error': 'Question text is required'}, status=400)
        
    question = Question.objects.create(task=task, text=text)
    return JsonResponse(question.to_dict(), status=201)

@csrf_exempt
def manage_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
        
    if request.method == 'PUT':
        data = json.loads(request.body)
        
        if 'answer' in data:
            question.answer = data['answer']
        if 'is_completed' in data:
            question.is_completed = bool(data['is_completed'])
            
        question.save()
        return JsonResponse(question.to_dict())
        
    elif request.method == 'DELETE':
        question.delete()
        return JsonResponse({'success': True})

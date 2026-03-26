#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

from django.test import Client
from tasks.models import Task

def test_backend():
    client = Client()
    
    print("🔍 Testing Backend Endpoints...")
    
    # Test main page
    response = client.get('/')
    print(f"✅ Main page: {response.status_code}")
    
    # Test AJAX create endpoint
    response = client.post('/ajax/create/', {
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'pending'
    })
    print(f"✅ AJAX Create: {response.status_code}")
    
    # Check if task was created
    task_count = Task.objects.count()
    print(f"✅ Tasks in database: {task_count}")
    
    if task_count > 0:
        task = Task.objects.first()
        print(f"✅ Sample task: {task.title} ({task.status})")
        
        # Test AJAX update
        response = client.post(f'/ajax/update/{task.id}/', {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'completed'
        })
        print(f"✅ AJAX Update: {response.status_code}")
        
        # Test AJAX delete
        response = client.post(f'/ajax/delete/{task.id}/')
        print(f"✅ AJAX Delete: {response.status_code}")
    
    print("🎉 Backend testing complete!")

if __name__ == '__main__':
    test_backend()

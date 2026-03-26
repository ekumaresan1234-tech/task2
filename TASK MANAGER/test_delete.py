#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

from django.test import Client
from tasks.models import Task

def test_delete_specifically():
    client = Client()
    
    print("🔍 Testing Delete Function Specifically...")
    
    # Create a test task first
    task = Task.objects.create(
        title='Test Task for Delete',
        description='This will be deleted',
        status='pending'
    )
    print(f"✅ Created test task: {task.id} - {task.title}")
    
    # Test delete endpoint
    response = client.post(f'/ajax/delete/{task.id}/', {
        'csrfmiddlewaretoken': 'test-token'
    })
    print(f"✅ Delete response status: {response.status_code}")
    print(f"✅ Delete response content: {response.content.decode()}")
    
    # Check if task still exists
    exists = Task.objects.filter(id=task.id).exists()
    print(f"✅ Task still exists: {exists}")
    
    # Test with proper CSRF
    response = client.get('/')
    csrf_token = client.cookies.get('csrftoken', '')
    print(f"✅ CSRF token from page: {csrf_token}")
    
    # Create another task
    task2 = Task.objects.create(
        title='Test Task for Delete 2',
        description='This will be deleted too',
        status='pending'
    )
    
    # Test delete with proper CSRF
    response = client.post(f'/ajax/delete/{task2.id}/', {
        'csrfmiddlewaretoken': csrf_token
    })
    print(f"✅ Delete with CSRF status: {response.status_code}")
    print(f"✅ Delete with CSRF content: {response.content.decode()}")
    
    exists2 = Task.objects.filter(id=task2.id).exists()
    print(f"✅ Task2 still exists: {exists2}")

if __name__ == '__main__':
    test_delete_specifically()

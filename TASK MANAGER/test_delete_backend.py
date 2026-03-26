#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()

from django.test import Client
from tasks.models import Task

def test_delete_backend():
    print("🔍 Testing Delete Backend Directly...")
    
    client = Client()
    
    # Check current tasks
    tasks = Task.objects.all()
    print(f"Current tasks count: {tasks.count()}")
    
    if tasks.count() == 0:
        # Create a test task
        task = Task.objects.create(
            title='Test Task for Delete',
            description='This will be deleted',
            status='pending'
        )
        print(f"Created test task: {task.id} - {task.title}")
    else:
        task = tasks.first()
        print(f"Using existing task: {task.id} - {task.title}")
    
    # Test the delete endpoint
    print(f"Testing delete of task {task.id}...")
    
    # Get the page first to get CSRF token
    response = client.get('/')
    print(f"Main page status: {response.status_code}")
    
    # Extract CSRF token
    csrf_token = ''
    if 'csrftoken' in client.cookies:
        csrf_token = client.cookies['csrftoken']
        print(f"CSRF token: {csrf_token[:20]}...")
    
    # Test delete with CSRF token
    response = client.post(f'/ajax/delete/{task.id}/', {
        'csrfmiddlewaretoken': csrf_token
    })
    
    print(f"Delete response status: {response.status_code}")
    print(f"Delete response content: {response.content.decode()}")
    
    # Check if task still exists
    exists = Task.objects.filter(id=task.id).exists()
    print(f"Task still exists after delete: {exists}")
    
    # Test delete without CSRF (since we have @csrf_exempt)
    if exists:
        response = client.post(f'/ajax/delete/{task.id}/')
        print(f"Delete without CSRF status: {response.status_code}")
        print(f"Delete without CSRF content: {response.content.decode()}")
        exists = Task.objects.filter(id=task.id).exists()
        print(f"Task exists after delete without CSRF: {exists}")

if __name__ == '__main__':
    test_delete_backend()

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_project.settings')
django.setup()

from tasks.models import Task

questions = [
    {
        "title": "Question 1: API Integration",
        "description": "How do you handle trailing slashes in Django POST requests?"
    },
    {
        "title": "Question 2: Database Management",
        "description": "What is the command to create an entirely new db.sqlite3 database schema from scratch?"
    },
    {
        "title": "Question 3: Frontend Fetch API",
        "description": "Explain how the fetch() API is used to send JSON payloads to a backend endpoint."
    },
    {
        "title": "Question 4: CORS Configuration",
        "description": "Why is django-cors-headers necessary when connecting a standalone frontend to a Django backend?"
    },
    {
        "title": "Question 5: UI Design",
        "description": "What CSS properties give a glassmorphism effect to a web container?"
    }
]

def seed_db():
    print("Clearing existing tasks...")
    Task.objects.all().delete()
    
    print("Adding 5 question tasks...")
    for q in questions:
        Task.objects.create(title=q["title"], description=q["description"])
        
    print(f"Successfully added {len(questions)} tasks to the database!")

if __name__ == '__main__':
    seed_db()

#!/usr/bin/env python
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
    
    import django
    from django.conf import settings
    
    print("✓ Django settings loaded successfully")
    print(f"✓ Django version: {django.get_version()}")
    print(f"✓ Debug mode: {settings.DEBUG}")
    print(f"✓ Database: {settings.DATABASES['default']['ENGINE']}")
    print(f"✓ Installed apps: {len(settings.INSTALLED_APPS)} apps")
    
    # Test importing the tasks app
    from tasks.models import Task
    print("✓ Tasks app imported successfully")
    
    print("\n🎉 All checks passed! The application should run properly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

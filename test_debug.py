#!/usr/bin/env python
import os
import sys

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Python path:", sys.path)

try:
    import django
    print("Django version:", django.get_version())
except ImportError as e:
    print("Django import error:", e)

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
    import django
    django.setup()
    print("Django setup successful")
except Exception as e:
    print("Django setup error:", e)
    import traceback
    traceback.print_exc()

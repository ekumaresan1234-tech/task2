from django.db import models
from django.utils import timezone

class Task(models.Model):
    # id field is created automatically by Django
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'tasks' # Maps to the existing 'tasks' table

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S') if self.created_date else None,
            'questions': [q.to_dict() for q in self.questions.all()]
        }

class Question(models.Model):
    task = models.ForeignKey(Task, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    answer = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'text': self.text,
            'answer': self.answer,
            'is_completed': self.is_completed,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S') if self.created_date else None
        }

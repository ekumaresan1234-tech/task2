from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="")
    status = models.CharField(max_length=20)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Trainee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TraineeProgress(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField()  # e.g., percentage of completion
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainee.name} - {self.training_module.title}"

class Exam(models.Model):
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    max_score = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainee.name} - {self.exam.title} - {self.score}"

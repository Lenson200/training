from django.db import models
from django.contrib.auth.models import AbstractUser
from PyPDF2 import PdfReader
# Create your models here.

class User(AbstractUser):
    is_trainee = models.BooleanField(default=False)

class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainee_profile', null=True, blank=True)
    name = models.CharField(max_length=100, default="John Doe")
    staffnumber = models.CharField(max_length=100, default='Q0001')
    Team=models.CharField(max_length=20, default="Team00")
    designation=models.CharField(max_length=60, default="Technician")
    Facility=models.CharField(max_length=15, default="cargo")
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name}, {self.staffnumber}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='uploads/profile_pics', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    total_pages = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    def update_total_pages(self):
        if self.file:
            with open(self.file.path, 'rb') as f:
                pdf_reader = PdfReader(f)
                self.total_pages = len(pdf_reader.pages)
                self.save()


class TraineeProgress(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField(default=0)
    progress = models.PositiveIntegerField(default=0)  # Updated automatically based on progress_ratio
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.total_modules > 0:
            self.progress = round((self.completed_modules / self.total_modules) * 100)
        else:
            self.progress = 0
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainee.name} - Progress: {self.progress}%"

class Exam(models.Model):
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    max_score = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainee.name} - {self.exam.title} - {self.score}"

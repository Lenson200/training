from django import forms
from .models import TrainingModule, TraineeProgress, Exam

class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description']

class TraineeProgressForm(forms.ModelForm):
    class Meta:
        model = TraineeProgress
        fields = ['trainee', 'training_module', 'progress']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['training_module', 'title', 'description', 'date', 'max_score']

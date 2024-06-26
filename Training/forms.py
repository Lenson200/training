from django import forms
from .models import TrainingModule, TraineeProgress, Exam

class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > 20*2024*2024:
                raise forms.ValidationError("File size must be under 20MB.")
            if not file.content_type in ['application/pdf', 'application/msword', 'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
                raise forms.ValidationError("File type is not supported.")
            return file

class TraineeProgressForm(forms.ModelForm):
    class Meta:
        model = TraineeProgress
        fields = ['trainee', 'training_module', 'progress']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['training_module', 'title', 'description', 'date', 'max_score']

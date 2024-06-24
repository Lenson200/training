from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import TrainingModule, TraineeProgress, Exam
from .forms import TrainingModuleForm, TraineeProgressForm, ExamForm
from PyPDF2 import PdfReader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'Training/training_module_list.html')
# Training Modules views
def training_module_list(request):
    training_modules = TrainingModule.objects.all()
    return render(request, 'Training/training_module_list.html', {'training_modules': training_modules})

def training_module_detail(request, pk):
    training_module = get_object_or_404(TrainingModule, pk=pk)

    if training_module.file:
        # Open the PDF file
        with open(training_module.file.path, 'rb') as f:
            pdf_reader = PdfReader(f)
            num_pages =  len(pdf_reader.pages) 

        # Update total_pages in the TrainingModule model
        if training_module.total_pages != num_pages:
            training_module.total_pages = num_pages
            training_module.save()

    return render(request, 'Training/trialview.html', {'training_module': training_module})

def training_module_create(request):
    if request.method == 'POST':
        form = TrainingModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('training_module_list')
    else:
        form = TrainingModuleForm()
    return render(request, 'Training/training_module_form.html', {'form': form})

def training_module_update(request, pk):
    training_module = get_object_or_404(TrainingModule, pk=pk)
    if request.method == 'POST':
        form = TrainingModuleForm(request.POST, request.FILES, instance=training_module)
        if form.is_valid():
            form.save()
            return redirect('training_module_list')
    else:
        form = TrainingModuleForm(instance=training_module)
    return render(request, 'Training/training_module_form.html', {'form': form, 'training_module': training_module})

def training_module_delete(request, pk):
    training_module = get_object_or_404(TrainingModule, pk=pk)
    if request.method == 'POST':
        training_module.delete()
        return redirect('training_module_list')
    return render(request, 'Training/training_module_confirm_delete.html', {'training_module': training_module})

# Trainee Progress views
@csrf_exempt
def mark_progress(request):#ajax for 
    if request.method == 'POST' and request.is_ajax():
        module_id = request.POST.get('module_id')
        trainee_id = request.POST.get('trainee_id')
        progress = request.POST.get('progress')

        # Retrieve or create TraineeProgress instance
        trainee_progress, created = TraineeProgress.objects.get_or_create(
            trainee_id=trainee_id,
            training_module_id=module_id,
            defaults={'progress': progress}
        )

        # Update progress if not created
        if not created:
            trainee_progress.progress = progress
            trainee_progress.save()

        return JsonResponse({'message': 'Progress updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
    
def trainee_progress_list(request):
    trainee_progress = TraineeProgress.objects.all()
    return render(request, 'Training/trainee_progress_list.html', {'trainee_progress': trainee_progress})

def trainee_progress_detail(request, pk):
    trainee_progress = get_object_or_404(TraineeProgress, pk=pk)
    return render(request, 'Training/trainee_progress_detail.html', {'trainee_progress': trainee_progress})

def trainee_progress_create(request):
    if request.method == 'POST':
        form = TraineeProgressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainee_progress_list')
    else:
        form = TraineeProgressForm()
    return render(request, 'Training/trainee_progress_form.html', {'form': form})

def trainee_progress_update(request, pk):
    trainee_progress = get_object_or_404(TraineeProgress, pk=pk)
    if request.method == 'POST':
        form = TraineeProgressForm(request.POST, instance=trainee_progress)
        if form.is_valid():
            form.save()
            return redirect('trainee_progress_list')
    else:
        form = TraineeProgressForm(instance=trainee_progress)
    return render(request, 'Training/trainee_progress_form.html', {'form': form, 'trainee_progress': trainee_progress})

def trainee_progress_delete(request, pk):
    trainee_progress = get_object_or_404(TraineeProgress, pk=pk)
    if request.method == 'POST':
        trainee_progress.delete()
        return redirect('trainee_progress_list')
    return render(request, 'Training/trainee_progress_confirm_delete.html', {'trainee_progress': trainee_progress})







# Exam views
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'Training/exam_list.html', {'exams': exams})

def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'Training/exam_detail.html', {'exam': exam})

def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'Training/exam_form.html', {'form': form})

def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'Training/exam_form.html', {'form': form, 'exam': exam})

def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam_list')
    return render(request, 'Training/exam_confirm_delete.html', {'exam': exam})

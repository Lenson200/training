from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import User,Trainee,UserProfile,TrainingModule, TraineeProgress, Exam
from .forms import TraineeUpdateForm,UserProfileForm,TrainingModuleForm, TraineeProgressForm,ExamForm
from PyPDF2 import PdfReader
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# import python_pptx  # For handling PPT files (install via pip if not already)
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request,'Training/training_module_list.html')

########### register,login & logout  views#######
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Redirect the user to the next URL if it exists
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')  # Redirect to index if next URL is not provided
        else:
            return render(request, "Training/login.html", {
                "message": "Invalid username and/or password.",
                "next": request.GET.get("next"),
            })
    else:
        return render(request, "Training/login.html", {"next": request.GET.get("next")})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Training/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Training/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Training/register.html")
    
@login_required
def update_trainee_profile(request):
    # Get the Trainee instance associated with the current user
    trainee = request.user.trainee_profile

    if request.method == 'POST':
        form = TraineeUpdateForm(request.POST, instance=trainee)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Replace with your URL name for profile updated
    else:
        form = TraineeUpdateForm(instance=trainee)

    return render(request, 'Training/create_trainee.html', {'form': form})

def success_page(request):
    return render(request, 'Training/success.html')

def update_profile(request):
    user = request.user
    
    # Get or create UserProfile instance for the user
    profile_instance, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile_instance)

        if profile_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user  # Ensure user is set
            profile_instance.save()

            # Ensure Trainee instance exists for the user
            trainee_profile, trainee_created = Trainee.objects.get_or_create(user=user)
            trainee_profile.save()

            # Update is_trainee to True
            user.is_trainee = True
            user.save()

            return redirect('success_page')  # Replace with your actual success URL
    else:
        profile_form = UserProfileForm(instance=profile_instance)
    
    return render(request, 'Training/update_profile.html', {'profile_form': profile_form})


# ##############################Training Modules views###############################

@login_required
def training_module_list(request):
    training_modules = TrainingModule.objects.all()
    return render(request, 'Training/training_module_list.html', {'training_modules': training_modules})

def training_module_detail(request, pk):
    training_module = get_object_or_404(TrainingModule, pk=pk)

    if training_module.file:
        file_extension = os.path.splitext(training_module.file.name)[1].lower()

        if file_extension == '.pdf':
            with open(training_module.file.path, 'rb') as f:
                pdf_reader = PdfReader(f)
                num_pages = len(pdf_reader.pages)

            if training_module.total_pages != num_pages:
                training_module.total_pages = num_pages
                training_module.save()

    return render(request, 'Training/training_module_detail.html', {
        'training_module': training_module,
        'page_range': range(1, training_module.total_pages + 1) if training_module.total_pages else None
    })


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
        return redirect('show_all')  # Redirect to the list view after deletion

    return render(request, 'Training/training_module_confirm_delete.html', {'training_module': training_module})

def show_all(request):
    training_modules = TrainingModule.objects.all()
    return render(request, 'Training/deletion_view.html', {'training_modules': training_modules})
#__________#########################################################################
# Trainee Progress views
@csrf_exempt
def mark_progress(request):#ajax for 
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        module_id = request.POST.get('module_id')
        trainee_id = request.POST.get('trainee_id')
        progress = int(request.POST.get('progress'))

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

@csrf_exempt  
def mark_module_complete(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        module_id = request.POST.get('module-id')
        trainee_id = request.POST.get('trainee-id')
        progress = request.POST.get('progress')
        
        # Get or create TraineeProgress object
        trainee_progress, created = TraineeProgress.objects.get_or_create(
            trainee_id=trainee_id,
            training_module_id=module_id,
            defaults={'progress': progress, 'completed': True, 'completion_date': timezone.now()}
        )
        
        # Determine if the module should be marked as complete
        if created:  # New entry created, definitely mark as complete
            trainee_progress.completed = True
            trainee_progress.completion_date = timezone.now()
            trainee_progress.save()
            message = 'Module marked as complete.'
        else:  # Entry already exists, decide based on logic if it should be marked complete
            # Example: Only mark as complete if progress is 100%
            if int(progress) == 100:
                trainee_progress.completed = True
                trainee_progress.completion_date = timezone.now()
                trainee_progress.save()
                message = 'Module marked as complete.'
            else:
                message = 'Module not marked as complete.'
        
        return JsonResponse({'message': message})
    else:
        return JsonResponse({'error': 'Invalid request'})

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

def exam_detail(request, pk, page=1):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all()[(page-1)*3:page*3]
    total_pages = (exam.questions.count() - 1) // 3 + 1
    return render(request, 'Training/Questions.html', {
        'exam': exam,
        'questions': questions,
        'page': page,
        'total_pages': total_pages
    })


def update_progress(request, exam_id, progress):
    exam = get_object_or_404(Exam, pk=exam_id)
    trainee = request.user  # Assume the trainee is the logged-in user
    trainee_progress, created = TraineeProgress.objects.get_or_create(trainee=trainee, exam=exam)
    trainee_progress.progress = progress
    trainee_progress.save()
    return JsonResponse({'status': 'ok'})

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

#other alternative 
# def training_module_detail(request, pk):
#     training_module = get_object_or_404(TrainingModule, pk=pk)

#     if training_module.file:
#         file_extension = os.path.splitext(training_module.file.name)[1].lower()

#         if file_extension == '.pdf':
#             # Handle PDF file
#             with open(training_module.file.path, 'rb') as f:
#                 pdf_reader = PdfReader(f)
#                 num_pages = len(pdf_reader.pages)

#             # Update total_pages in the TrainingModule model if necessary
#             if training_module.total_pages != num_pages:
#                 training_module.total_pages = num_pages
#                 training_module.save()

#         elif file_extension == '.pptx':
#             # Handle PPTX file (convert to PDF for rendering)
#             pptx_path = training_module.file.path
#             # pptx = python_pptx.Presentation(pptx_path)

#             # Example: Convert each slide to a PDF page
#             # You'll need to implement actual conversion logic based on your requirements

#         elif file_extension == '.docx':
#             # Handle DOCX file (convert to PDF for rendering)
#             docx_path = training_module.file.path
#             # doc = Document(docx_path)

#             # Example: Convert DOCX content to PDF
#             # You'll need to implement actual conversion logic based on your requirements

#     return render(request, 'Training/trialview.html', {
#         'training_module': training_module,
#         'page_range': range(1, training_module.total_pages + 1) if training_module.total_pages else None
#     })

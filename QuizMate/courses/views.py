from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import CustomUser, Course, Enrollment, Quiz, Question, Submission


def home(request):
    return render(request, 'courses/home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            if user_type == 'student':
                user.is_student = True
            elif user_type == 'instructor':
                user.is_instructor = True
            user.save()
            login(request, user)
            return redirect('student_dashboard' if user.is_student else 'instructor_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard' if user.is_student else 'instructor_dashboard')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def student_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_student:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'courses/student_dashboard.html', {'courses': courses})

def instructor_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    courses = Course.objects.filter(instructor=request.user)
    total_students = CustomUser.objects.filter(enrollments__course__in=courses).distinct().count()
    
    context = {
        'courses': courses,
        'total_students': total_students,
        'students': CustomUser.objects.filter(enrollments__course__in=courses)
    }
    return render(request, 'courses/instructor_dashboard.html', context)
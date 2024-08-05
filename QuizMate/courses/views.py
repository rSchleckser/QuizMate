from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course, Enrollment, Quiz, Question, Submission


def home(request):
    return render(request, 'courses/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard' if user.is_student else 'instructor_dashboard')
    else:
        form = UserCreationForm()
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
    return redirect('courses/home')

def student_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_student:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'courses/student_dashboard.html', {'courses': courses})

def instructor_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor_dashboard.html', {'courses': courses})
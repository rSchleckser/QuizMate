from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CourseForm
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
    return render(request, 'courses/student/student_dashboard.html', {'courses': courses})

def instructor_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    courses = Course.objects.filter(instructor=request.user)
    total_students = CustomUser.objects.filter(enrollments__course__in=courses).distinct().count()
    
    context = {
        'courses': courses,
        'total_students': total_students,
        'students': CustomUser.objects.filter(enrollments__course__in=courses),
        'user_type': 'Instructor'  
    }
    return render(request, 'courses/instructor/instructor_dashboard.html', context)

# POST 
def course_create(request):
    if request.method == 'POST':
       form = CourseForm(request.POST)
       if form.is_valid():
          course = form.save(commit=False)
          course.instructor = request.user 
          course.save() 
          return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/instructor/course_form.html', {'form': form})

# EDIT
def course_edit(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/instructor/course_form.html', {'form': form})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail_student(request, pk):
    course = Course.objects.get(id=pk)
    quizzes = Quiz.objects.filter(course=course)
    return render(request, 'courses/student/course_detail_student.html', {'course': course, 'quizzes': quizzes})

def course_detail_instructor(request, pk):
    course = Course.objects.get(id=pk)
    students = Enrollment.objects.filter(course=course)
    return render(request, 'courses/instructor/course_detail_instructor.html', {'course': course, 'students': students})


def enrolled_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [enrollment.course for enrollment in enrollments]
    return render(request, 'courses/student/enrolled_courses.html', {'courses': courses})
from django.shortcuts import render, redirect,  redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CourseForm, QuizForm, QuestionForm
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
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
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
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    course = Course.objects.get(pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/instructor/course_form.html', {'form': form})

# DELETE
def course_delete(request, pk):
    Course.objects.get(id=pk).delete()
    return redirect('instructor_dashboard')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# =========== COURSE ENROLLMENT ===========
def course_enrollment(request, pk):
    if not request.user.is_student:
        return redirect('login')  
    course = Course.objects.get(id=pk)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('student_dashboard')

def course_unenroll(request, pk):
    if not request.user.is_student:
        return redirect('login')
    course = Course.objects.get(id=pk)
    enrollment = Enrollment.objects.get(student=request.user, course=course)
    enrollment.delete()

    return redirect('student_dashboard')


# =========== COURSE DETAILS ==============

# Instructors 
def course_detail_instructor(request, pk):
    course = Course.objects.get(id=pk)
    students = Enrollment.objects.filter(course=course)
    quizzes = course.quizzes.all()
    return render(request, 'courses/instructor/course_detail_instructor.html', {'course': course, 'students': students, 'quizzes': quizzes,})
    
# Instructor Quiz
def quiz_detail_instructor(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = quiz.questions.all()
    return render(request, 'courses/instructor/quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

def quiz_create(request, pk):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')

    course = Course.objects.get(id=pk)

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect('course_detail_instructor', pk=course.pk)
    else:
        form = QuizForm()

    return render(request, 'courses/instructor/quiz/quiz_form.html', {'form': form, 'course': course})

def quiz_edit(request, pk):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            return redirect('quiz_detail_instructor', pk= quiz.pk)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'courses/instructor/quiz/quiz_form.html', {'form': form})

def quiz_delete(request, pk, course_pk):
    quiz = Quiz.objects.get(pk=pk).delete()
    return redirect('course_detail_instructor',pk = course_pk)

# Instructor Questions
def question_create(request, pk):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    quiz = Quiz.objects.get(id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz_detail_instructor', pk=quiz.pk)  
    else:
        form = QuestionForm()

    return render(request, 'courses/instructor/quiz/question_form.html', {'form': form, 'quiz': quiz})

def question_edit(request, pk, quiz_pk):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('quiz_detail_instructor', pk = quiz_pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'courses/instructor/quiz/question_form.html', {'form': form})

def question_delete(request, pk, quiz_pk):
    question = Question.objects.get(pk=pk).delete()
    return redirect('quiz_detail_instructor', pk = quiz_pk)


# Students
def course_detail_student(request, pk):
    course = Course.objects.get(id=pk)
    quizzes = Quiz.objects.filter(course=course)
    return render(request, 'courses/student/course_detail_student.html', {'course': course, 'quizzes': quizzes})

def take_quiz(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        student_answers = []

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            is_correct = question.is_correct(selected_option)
            if selected_option and is_correct:
                score += 1
            student_answers.append({
                'question': question,
                'selected_option': selected_option,
                'is_correct': is_correct
            })

        percentage = (score / total_questions) * 100
        feedback = f'You scored {score} out of {total_questions} ({percentage:.2f}%).'

    
        Submission.objects.create(student=request.user, quiz=quiz, score=score)

        return render(request, 'courses/student/quiz/quiz_result.html', {
            'course': course,
            'quiz': quiz,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'feedback': feedback,
            'student_answers': student_answers,
        })
    return render(request, 'courses/student/quiz/take_quiz.html', {'course': course, 'quiz': quiz})


def quiz_result(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = request.GET.get('score')
    total_questions = request.GET.get('total_questions')
    percentage = request.GET.get('percentage')
    feedback = request.GET.get('feedback')
    student_answers = request.GET.get('student_answers')

    return render(request, 'courses/student/quiz/quiz_result.html', {
        'course': course,
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'feedback': feedback,
        'student_answers': student_answers,
    })



def enrolled_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    courses = [enrollment.course for enrollment in enrollments]
    return render(request, 'courses/student/enrolled_courses.html', {'courses': courses})
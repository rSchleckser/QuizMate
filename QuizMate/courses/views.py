from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CourseForm, QuizForm, QuestionForm
from .models import CustomUser, Course, Enrollment, Quiz, Question, Submission
from django.db.models import Max, Count, Avg


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
    student= request.user
    available_courses = Course.objects.exclude(enrollments__student=request.user)
    enrolled_courses = Enrollment.objects.filter(student=request.user)

    return render(request, 'courses/student/student_dashboard.html', {
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
        'student': student,
    })

def student_detail(request, student_id):
    
    student = CustomUser.objects.get(id=student_id)
    enrollments = Enrollment.objects.filter(student=student)

    avg_grade = enrollments.aggregate(avg_grade=Avg('grade'))['avg_grade']
    avg_progress = enrollments.aggregate(avg_progress=Avg('progress'))['avg_progress']
   
    return render(request, 'courses/instructor/student_detail.html', {
            'student': student,
            'enrollments': enrollments,
            'avg_grade': avg_grade,
            'avg_progress': avg_progress,
        })

def student_profile(request, student_id):
    
    student = CustomUser.objects.get(id=student_id)
    enrollments = Enrollment.objects.filter(student=student)

    avg_grade = enrollments.aggregate(avg_grade=Avg('grade'))['avg_grade']
    avg_progress = enrollments.aggregate(avg_progress=Avg('progress'))['avg_progress']
   
    return render(request, 'courses/student/student_profile.html', {
            'student': student,
            'enrollments': enrollments,
            'avg_grade': avg_grade,
            'avg_progress': avg_progress,
        })



def instructor_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return redirect('login')
    courses = Course.objects.filter(instructor=request.user)
    total_students = CustomUser.objects.filter(enrollments__course__in=courses).count()
   
    
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
    if not request.user.is_authenticated or not request.user.is_student:
        return redirect('login')
    student= request.user
    course = Course.objects.get(id=pk)
    quizzes = Quiz.objects.filter(course=course)
    submissions = Submission.objects.filter(student=request.user)

    latest_submissions = (
        Submission.objects.filter(student=request.user, quiz__in=quizzes)
        .values('quiz')
        .annotate(latest_submission_id=Max('id'))
    )
    user_submissions = Submission.objects.filter(id__in=[sub['latest_submission_id'] for sub in latest_submissions])
    
    quizzes_taken = user_submissions.count()
    number_of_submissions = submissions.count()
    quizzes_completed = quizzes.count()

    average_percentage = (
        sum(sub.percentage() for sub in user_submissions) / len(user_submissions)
        if user_submissions else 0
    )
    
    quizzes_completed_percentage = (quizzes_taken / quizzes_completed * 100) if quizzes_completed > 0 else 0
    quizzes_completed_percentage = "{:.2f}".format(quizzes_completed_percentage)

    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        enrollment.progress = quizzes_completed_percentage
        enrollment.grade = average_percentage
        enrollment.save()
    except Enrollment.DoesNotExist:
        pass
    
    return render(request, 'courses/student/course_detail_student.html', {
        'student':student,
        'course': course,
        'quizzes': quizzes,
        'user_submissions': user_submissions,
        'number_of_quizzes_taken': quizzes_taken,
        'number_of_submissions': number_of_submissions,
        'average_percentage': round(average_percentage, 2),
        'quizzes_completed_percentage': quizzes_completed_percentage
    })
    



def take_quiz(request, course_id, quiz_id):
    student= request.user
    course = Course.objects.get(id=course_id)
    quiz = Quiz.objects.get(id=quiz_id)
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
        Submission.objects.create(student=request.user, quiz=quiz, score=score, total_questions=total_questions)

        return render(request, 'courses/student/quiz/quiz_result.html', {
            'student':student,
            'course': course,
            'quiz': quiz,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'feedback': feedback,
            'student_answers': student_answers,
        })
    
    return render(request, 'courses/student/quiz/take_quiz.html', {'course': course, 'quiz': quiz,'student':student, })


def quiz_result(request, course_id, quiz_id):
    course = Course.objects.get(id=course_id)
    quiz = Quiz.objects.get(id=quiz_id)
    
    return render(request, 'courses/student/quiz/quiz_result.html', {
        'course': course,
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'feedback': feedback,
        'student_answers': student_answers,
    })



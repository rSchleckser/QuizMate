from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import PermissionDenied
from django.db.models import Max, Avg

from .decorators import instructor_required, student_required
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

@student_required
def student_dashboard(request):
    student = request.user
    available_courses = Course.objects.exclude(enrollments__student=request.user)
    enrolled_courses = Enrollment.objects.filter(student=request.user)

    return render(request, 'courses/student/student_dashboard.html', {
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
        'student': student,
    })

@instructor_required
def student_detail(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    enrollments = Enrollment.objects.filter(student=student)

    avg_grade = enrollments.aggregate(avg_grade=Avg('grade'))['avg_grade']
    avg_progress = enrollments.aggregate(avg_progress=Avg('progress'))['avg_progress']

    return render(request, 'courses/instructor/student_detail.html', {
            'student': student,
            'enrollments': enrollments,
            'avg_grade': avg_grade,
            'avg_progress': avg_progress,
        })

@student_required
def student_profile(request, student_id):
    if request.user.id != student_id:
        raise PermissionDenied

    student = get_object_or_404(CustomUser, id=student_id)
    enrollments = Enrollment.objects.filter(student=student)

    avg_grade = enrollments.aggregate(avg_grade=Avg('grade'))['avg_grade']
    avg_progress = enrollments.aggregate(avg_progress=Avg('progress'))['avg_progress']

    return render(request, 'courses/student/student_profile.html', {
            'student': student,
            'enrollments': enrollments,
            'avg_grade': avg_grade,
            'avg_progress': avg_progress,
        })


@instructor_required
def instructor_dashboard(request):
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
@instructor_required
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
@instructor_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.instructor != request.user:
        raise PermissionDenied
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/instructor/course_form.html', {'form': form})

# DELETE
@instructor_required
def course_delete(request, pk):
    course = get_object_or_404(Course, id=pk)
    if course.instructor != request.user:
        raise PermissionDenied
    course.delete()
    return redirect('instructor_dashboard')



# =========== COURSE ENROLLMENT ===========
@student_required
def course_enrollment(request, pk):
    course = get_object_or_404(Course, id=pk)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('student_dashboard')

@student_required
def course_unenroll(request, pk):
    course = get_object_or_404(Course, id=pk)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    enrollment.delete()

    return redirect('student_dashboard')


# =========== COURSE DETAILS ==============

# Instructors
@instructor_required
def course_detail_instructor(request, pk):
    course = get_object_or_404(Course, id=pk)
    if course.instructor != request.user:
        raise PermissionDenied
    students = Enrollment.objects.filter(course=course)
    quizzes = course.quizzes.all()
    return render(request, 'courses/instructor/course_detail_instructor.html', {'course': course, 'students': students, 'quizzes': quizzes,})

# Instructor Quiz
@instructor_required
def quiz_detail_instructor(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    if quiz.course.instructor != request.user:
        raise PermissionDenied
    questions = quiz.questions.all()
    return render(request, 'courses/instructor/quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

@instructor_required
def quiz_create(request, pk):
    course = get_object_or_404(Course, id=pk)
    if course.instructor != request.user:
        raise PermissionDenied

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

@instructor_required
def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if quiz.course.instructor != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            return redirect('quiz_detail_instructor', pk=quiz.pk)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'courses/instructor/quiz/quiz_form.html', {'form': form})

@instructor_required
def quiz_delete(request, pk, course_pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if quiz.course.instructor != request.user:
        raise PermissionDenied
    quiz.delete()
    return redirect('course_detail_instructor', pk=course_pk)

# Instructor Questions
@instructor_required
def question_create(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    if quiz.course.instructor != request.user:
        raise PermissionDenied
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

@instructor_required
def question_edit(request, pk, quiz_pk):
    question = get_object_or_404(Question, pk=pk)
    if question.quiz.course.instructor != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('quiz_detail_instructor', pk=quiz_pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'courses/instructor/quiz/question_form.html', {'form': form})

@instructor_required
def question_delete(request, pk, quiz_pk):
    question = get_object_or_404(Question, pk=pk)
    if question.quiz.course.instructor != request.user:
        raise PermissionDenied
    question.delete()
    return redirect('quiz_detail_instructor', pk=quiz_pk)


# Students
@student_required
def course_detail_student(request, pk):
    student = request.user
    course = get_object_or_404(Course, id=pk)
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

    return render(request, 'courses/student/course_detail_student.html', {
        'student': student,
        'course': course,
        'quizzes': quizzes,
        'user_submissions': user_submissions,
        'number_of_quizzes_taken': quizzes_taken,
        'number_of_submissions': number_of_submissions,
        'average_percentage': round(average_percentage, 2),
        'quizzes_completed_percentage': quizzes_completed_percentage
    })


@student_required
def take_quiz(request, course_id, quiz_id):
    student = request.user
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
        Submission.objects.create(student=request.user, quiz=quiz, score=score, total_questions=total_questions)

        _update_course_progress(request.user, course)

        return render(request, 'courses/student/quiz/quiz_result.html', {
            'student': student,
            'course': course,
            'quiz': quiz,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'feedback': feedback,
            'student_answers': student_answers,
        })

    return render(request, 'courses/student/quiz/take_quiz.html', {'course': course, 'quiz': quiz, 'student': student, })


def _update_course_progress(student, course):
    """Recompute and persist a student's grade/progress for a course after a quiz submission."""
    quizzes = Quiz.objects.filter(course=course)

    latest_submissions = (
        Submission.objects.filter(student=student, quiz__in=quizzes)
        .values('quiz')
        .annotate(latest_submission_id=Max('id'))
    )
    user_submissions = Submission.objects.filter(id__in=[sub['latest_submission_id'] for sub in latest_submissions])

    quizzes_taken = user_submissions.count()
    quizzes_completed = quizzes.count()

    average_percentage = (
        sum(sub.percentage() for sub in user_submissions) / len(user_submissions)
        if user_submissions else 0
    )
    quizzes_completed_percentage = (quizzes_taken / quizzes_completed * 100) if quizzes_completed > 0 else 0

    Enrollment.objects.filter(student=student, course=course).update(
        progress=quizzes_completed_percentage,
        grade=average_percentage,
    )

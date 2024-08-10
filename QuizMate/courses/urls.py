from django.urls import path
from . import views

urlpatterns = [
# Home and Auth Routes
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

# Instructor and Student Dashboard
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),

# Instructor Course CRUD
    path('instructor/course/<int:pk>/', views.course_detail_instructor, name='course_detail_instructor'),
    path('instructor/new_course/', views.course_create, name='course_create'),
    path('instructor/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('instructor/<int:pk>/delete/', views.course_delete, name='course_delete'),

# Instructor Course Quiz CRUD
    path('quiz/<int:pk>/', views.quiz_detail_instructor, name='quiz_detail_instructor'),
    path('instructor/course/<int:pk>/quiz/create/', views.quiz_create, name='quiz_create'),
    path('instructor/course/<int:pk>/quiz/edit/', views.quiz_edit, name='quiz_edit'),
    path('instructor/course/<int:course_pk>/quiz/<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),
    
# Instructor Course Question CRUD
    path('quiz/<int:pk>/question/create/', views.question_create, name='question_create'),
    path('quiz/<int:quiz_pk>/question/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('quiz/<int:quiz_pk>/question/<int:pk>/delete/', views.question_delete, name='question_delete'),


# Student Quiz
   path('student/course/<int:course_id>/quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('course/<int:course_id>/quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),

# Courses
# View Student's Specific course
    path('student/course/<int:pk>/', views.course_detail_student, name='course_detail_student'),

# Student Course Enrollment
    path('enroll/<int:pk>/', views.course_enrollment, name='course_enrollment'),
    path('unenroll/<int:pk>/', views.course_unenroll, name='course_unenroll'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/enrolled/', views.enrolled_courses, name='enrolled_courses'),

]
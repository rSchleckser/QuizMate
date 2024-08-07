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

# Instructor Course CRUD
    path('instructor/course/<int:pk>/', views.course_detail_instructor, name='course_detail_instructor'),
    path('instructor/new_course/', views.course_create, name='course_create'),
    path('instructor/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('instructor/<int:pk>/delete/', views.course_delete, name='course_delete'),

# Courses
    path('courses/', views.course_list, name='course_list'),
    path('student/course/<int:pk>/', views.course_detail_student, name='course_detail_student'),
    path('courses/enrolled/', views.enrolled_courses, name='enrolled_courses'),

]
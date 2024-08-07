from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('student/course/<int:pk>/', views.course_detail_student, name='course_detail_student'),
    path('instructor/course/<int:pk>/', views.course_detail_instructor, name='course_detail_instructor'),

    path('instructor/new_course/', views.course_create, name='course_create'),
    path('instructor/<int:pk>/edit/', views.course_edit, name='course_edit'),

    path('courses/', views.course_list, name='course_list'),



    path('courses/enrolled/', views.enrolled_courses, name='enrolled_courses'),

    # path('instructor/course/<int:course_id>/', views.course_detail_instructor, name='course_detail_instructor'),
]
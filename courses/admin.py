from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Course, Enrollment, Quiz, Question, Submission

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Submission)




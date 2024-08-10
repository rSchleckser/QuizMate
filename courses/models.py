from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)

    def avg_grade(self):
        return self.enrollments.aggregate(Avg('grade'))['grade__avg'] or 0.0

    def avg_progress(self):
        return self.enrollments.aggregate(Avg('progress'))['progress__avg'] or 0.0

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    image = models.CharField(max_length=200, null=True)

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    grade = models.FloatField(default= 0.0)
    progress = models.FloatField(default=0.0)

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=100)
    description = models.TextField()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100, default='Answer')

    def is_correct(self, selected_option):
        return str(self.correct_option) == str(selected_option)
    def get_correct_answer(self):
        return getattr(self, f'option{self.correct_option}')


class Submission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    score = models.FloatField()
    total_questions = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        if self.total_questions > 0:
            return (self.score / self.total_questions) * 100
        else:
            return 0  

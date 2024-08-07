from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Course, Enrollment, Quiz, Question

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('student', 'I am a student'),
        ('instructor', 'I am an instructor'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description','image')
        
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_option']

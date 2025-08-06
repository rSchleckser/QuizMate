# QuizMate Forms Documentation

## Table of Contents

1. [Forms Overview](#forms-overview)
2. [CustomUserCreationForm](#customusercreationform)
3. [CourseForm](#courseform)
4. [QuizForm](#quizform)
5. [QuestionForm](#questionform)
6. [Form Validation](#form-validation)
7. [Frontend Integration](#frontend-integration)
8. [Security Considerations](#security-considerations)
9. [Usage Examples](#usage-examples)

---

## Forms Overview

The QuizMate application uses 4 main form classes to handle user input:

- **CustomUserCreationForm**: User registration with role selection
- **CourseForm**: Course creation and editing
- **QuizForm**: Quiz creation and editing  
- **QuestionForm**: Question creation and editing

All forms extend Django's built-in form classes and include Bootstrap styling for consistent UI presentation.

---

## CustomUserCreationForm

**Location**: `courses/forms.py:5-16`
**Extends**: `UserCreationForm`
**Model**: `CustomUser`

### Description
Handles user registration with role-based account creation. Extends Django's default `UserCreationForm` to include user type selection.

### Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `username` | `CharField` | Unique username | Inherited from UserCreationForm |
| `password1` | `CharField` | Password | Inherited from UserCreationForm |
| `password2` | `CharField` | Password confirmation | Must match password1 |
| `user_type` | `ChoiceField` | User role selection | Required, must be 'student' or 'instructor' |

### User Type Choices

```python
USER_TYPE_CHOICES = [
    ('student', 'I am a student'),
    ('instructor', 'I am an instructor'),
]
```

### Widget Configuration

```python
user_type = forms.ChoiceField(
    choices=USER_TYPE_CHOICES, 
    widget=forms.RadioSelect
)
```

### Form Structure

```python
class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('student', 'I am a student'),
        ('instructor', 'I am an instructor'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields
```

### Usage in Views

```python
# In signup view
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
```

### Frontend Rendering

```html
<!-- In registration/signup.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign Up</button>
</form>
```

### Validation Rules

1. **Username**: Must be unique, follows Django's default username validation
2. **Password**: Must meet Django's default password requirements
3. **Password Confirmation**: Must match the first password
4. **User Type**: Must be either 'student' or 'instructor'

---

## CourseForm

**Location**: `courses/forms.py:17-25`
**Extends**: `ModelForm`
**Model**: `Course`

### Description
Handles course creation and editing for instructors. Includes Bootstrap styling for form controls.

### Fields

| Field | Type | Description | Validation | Widget |
|-------|------|-------------|------------|--------|
| `name` | `CharField` | Course name | Required, max 100 chars | `TextInput` with Bootstrap class |
| `description` | `TextField` | Course description | Required | `Textarea` with Bootstrap class |
| `image` | `CharField` | Course image filename | Optional, max 200 chars | Default |

### Form Structure

```python
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
```

### Bootstrap Integration

The form includes Bootstrap CSS classes for consistent styling:
- `form-control` class applied to text inputs and textareas
- Integrates with Bootstrap form layouts

### Usage in Views

```python
# Create course
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

# Edit course
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
```

### Frontend Rendering

```html
<!-- In courses/instructor/course_form.html -->
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label for="{{ form.name.id_for_label }}">Course Name</label>
        {{ form.name }}
    </div>
    <div class="form-group">
        <label for="{{ form.description.id_for_label }}">Description</label>
        {{ form.description }}
    </div>
    <div class="form-group">
        <label for="{{ form.image.id_for_label }}">Image</label>
        {{ form.image }}
    </div>
    <button type="submit" class="btn btn-primary">Save Course</button>
</form>
```

### Validation Rules

1. **Name**: Required, maximum 100 characters
2. **Description**: Required, no length limit
3. **Image**: Optional, maximum 200 characters

---

## QuizForm

**Location**: `courses/forms.py:26-33`
**Extends**: `ModelForm`
**Model**: `Quiz`

### Description
Handles quiz creation and editing within courses. Similar structure to CourseForm with Bootstrap styling.

### Fields

| Field | Type | Description | Validation | Widget |
|-------|------|-------------|------------|--------|
| `title` | `CharField` | Quiz title | Required, max 100 chars | `TextInput` with Bootstrap class |
| `description` | `TextField` | Quiz description | Required | `Textarea` with Bootstrap class |

### Form Structure

```python
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
```

### Usage in Views

```python
# Create quiz
def quiz_create(request, pk):
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

# Edit quiz
def quiz_edit(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            return redirect('quiz_detail_instructor', pk=quiz.pk)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'courses/instructor/quiz/quiz_form.html', {'form': form})
```

### Frontend Rendering

```html
<!-- In courses/instructor/quiz/quiz_form.html -->
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label for="{{ form.title.id_for_label }}">Quiz Title</label>
        {{ form.title }}
    </div>
    <div class="form-group">
        <label for="{{ form.description.id_for_label }}">Description</label>
        {{ form.description }}
    </div>
    <button type="submit" class="btn btn-primary">Save Quiz</button>
</form>
```

### Validation Rules

1. **Title**: Required, maximum 100 characters
2. **Description**: Required, no length limit

---

## QuestionForm

**Location**: `courses/forms.py:35-39`
**Extends**: `ModelForm`
**Model**: `Question`

### Description
Handles creation and editing of multiple-choice questions for quizzes. Does not include custom widgets but uses default form rendering.

### Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `question` | `CharField` | Question text | Required, max 255 chars |
| `option1` | `CharField` | First answer option | Required, max 100 chars |
| `option2` | `CharField` | Second answer option | Required, max 100 chars |
| `option3` | `CharField` | Third answer option | Required, max 100 chars |
| `option4` | `CharField` | Fourth answer option | Required, max 100 chars |
| `correct_option` | `CharField` | Correct answer (1-4) | Required, max 100 chars |

### Form Structure

```python
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_option']
```

### Usage in Views

```python
# Create question
def question_create(request, pk):
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

# Edit question
def question_edit(request, pk, quiz_pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('quiz_detail_instructor', pk=quiz_pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'courses/instructor/quiz/question_form.html', {'form': form})
```

### Frontend Rendering

```html
<!-- In courses/instructor/quiz/question_form.html -->
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label for="{{ form.question.id_for_label }}">Question</label>
        {{ form.question }}
    </div>
    <div class="row">
        <div class="col-md-6">
            <div class="form-group">
                <label for="{{ form.option1.id_for_label }}">Option 1</label>
                {{ form.option1 }}
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-group">
                <label for="{{ form.option2.id_for_label }}">Option 2</label>
                {{ form.option2 }}
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <div class="form-group">
                <label for="{{ form.option3.id_for_label }}">Option 3</label>
                {{ form.option3 }}
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-group">
                <label for="{{ form.option4.id_for_label }}">Option 4</label>
                {{ form.option4 }}
            </div>
        </div>
    </div>
    <div class="form-group">
        <label for="{{ form.correct_option.id_for_label }}">Correct Option (1-4)</label>
        {{ form.correct_option }}
    </div>
    <button type="submit" class="btn btn-primary">Save Question</button>
</form>
```

### Validation Rules

1. **Question**: Required, maximum 255 characters
2. **Options 1-4**: All required, maximum 100 characters each
3. **Correct Option**: Required, should be '1', '2', '3', or '4'

### Improvement Opportunities

The QuestionForm could be enhanced with:

```python
class QuestionForm(forms.ModelForm):
    CORRECT_OPTION_CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
    ]
    
    correct_option = forms.ChoiceField(
        choices=CORRECT_OPTION_CHOICES,
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = Question
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_option']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'option1': forms.TextInput(attrs={'class': 'form-control'}),
            'option2': forms.TextInput(attrs={'class': 'form-control'}),
            'option3': forms.TextInput(attrs={'class': 'form-control'}),
            'option4': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

---

## Form Validation

### Client-Side Validation

The forms rely primarily on HTML5 validation and Bootstrap styling for user feedback:

```html
<input type="text" class="form-control" required maxlength="100">
<textarea class="form-control" required></textarea>
```

### Server-Side Validation

Django provides comprehensive server-side validation:

1. **Field Type Validation**: Ensures data types match field definitions
2. **Length Validation**: Enforces maximum character limits
3. **Required Field Validation**: Ensures required fields are not empty
4. **Custom Validation**: Can be added through form methods

### Custom Validation Examples

```python
class CourseForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if Course.objects.filter(name=name, instructor=self.instance.instructor).exists():
            raise forms.ValidationError("You already have a course with this name.")
        return name
    
    def clean_image(self):
        image = self.cleaned_data['image']
        if image and not image.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise forms.ValidationError("Please provide a valid image file extension.")
        return image

class QuestionForm(forms.ModelForm):
    def clean_correct_option(self):
        correct_option = self.cleaned_data['correct_option']
        if correct_option not in ['1', '2', '3', '4']:
            raise forms.ValidationError("Correct option must be 1, 2, 3, or 4.")
        return correct_option
```

### Error Handling

Forms display validation errors in templates:

```html
<!-- Display form errors -->
{% if form.errors %}
    <div class="alert alert-danger">
        {{ form.errors }}
    </div>
{% endif %}

<!-- Display field-specific errors -->
<div class="form-group">
    <label for="{{ form.name.id_for_label }}">Course Name</label>
    {{ form.name }}
    {% if form.name.errors %}
        <div class="invalid-feedback d-block">
            {{ form.name.errors }}
        </div>
    {% endif %}
</div>
```

---

## Frontend Integration

### Bootstrap Styling

All forms integrate with Bootstrap 4/5 for consistent styling:

```css
.form-control {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
}

.form-control:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
```

### JavaScript Enhancement

Consider adding JavaScript for enhanced UX:

```javascript
// Real-time validation feedback
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Question form enhancements
function highlightCorrectOption() {
    const correctOption = document.getElementById('id_correct_option');
    const options = ['id_option1', 'id_option2', 'id_option3', 'id_option4'];
    
    correctOption.addEventListener('change', function() {
        options.forEach((optionId, index) => {
            const element = document.getElementById(optionId);
            if (this.value === (index + 1).toString()) {
                element.style.backgroundColor = '#d4edda';
            } else {
                element.style.backgroundColor = '';
            }
        });
    });
}
```

---

## Security Considerations

### CSRF Protection

All forms include CSRF tokens:

```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Input Sanitization

Django automatically escapes user input in templates:

```html
<!-- Safe - automatically escaped -->
<p>{{ form.cleaned_data.name }}</p>

<!-- Unsafe - only use with trusted data -->
<p>{{ form.cleaned_data.name|safe }}</p>
```

### File Upload Security

For image uploads, implement proper validation:

```python
class CourseForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if not any(image.lower().endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("Invalid file type.")
            
            # Validate file size (if uploading actual files)
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("File too large.")
        
        return image
```

### SQL Injection Prevention

Django ORM prevents SQL injection, but be cautious with raw queries:

```python
# Safe - uses parameterized queries
Course.objects.filter(name__icontains=search_term)

# Unsafe - don't do this
Course.objects.extra(where=["name LIKE '%{}%'".format(search_term)])
```

---

## Usage Examples

### Complete Form Integration Example

```python
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CourseForm
from .models import Course

@login_required
def course_create(request):
    if not request.user.is_instructor:
        messages.error(request, "Only instructors can create courses.")
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f"Course '{course.name}' created successfully!")
            return redirect('instructor_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseForm()
    
    return render(request, 'courses/instructor/course_form.html', {
        'form': form,
        'title': 'Create New Course'
    })

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.name}' updated successfully!")
            return redirect('course_detail_instructor', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/instructor/course_form.html', {
        'form': form,
        'course': course,
        'title': f'Edit {course.name}'
    })
```

### Advanced Template Integration

```html
<!-- courses/instructor/course_form.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h3>{{ title }}</h3>
                </div>
                <div class="card-body">
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                                {{ message }}
                                <button type="button" class="close" data-dismiss="alert">
                                    <span>&times;</span>
                                </button>
                            </div>
                        {% endfor %}
                    {% endif %}

                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        <div class="form-group">
                            <label for="{{ form.name.id_for_label }}">
                                Course Name <span class="text-danger">*</span>
                            </label>
                            {{ form.name }}
                            {% if form.name.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.name.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>

                        <div class="form-group">
                            <label for="{{ form.description.id_for_label }}">
                                Description <span class="text-danger">*</span>
                            </label>
                            {{ form.description }}
                            {% if form.description.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.description.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>

                        <div class="form-group">
                            <label for="{{ form.image.id_for_label }}">Course Image</label>
                            {{ form.image }}
                            <small class="form-text text-muted">
                                Optional. Provide filename for course image (e.g., python.jpg)
                            </small>
                            {% if form.image.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.image.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>

                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">
                                {% if course %}Update Course{% else %}Create Course{% endif %}
                            </button>
                            <a href="{% url 'instructor_dashboard' %}" class="btn btn-secondary ml-2">
                                Cancel
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap validation classes
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});
</script>
{% endblock %}
```

### Form Testing Examples

```python
# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.forms import CustomUserCreationForm, CourseForm, QuizForm, QuestionForm
from courses.models import Course, Quiz

User = get_user_model()

class CustomUserCreationFormTest(TestCase):
    def test_valid_student_registration(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'user_type': 'student'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_user_type(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'user_type': 'invalid'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

class CourseFormTest(TestCase):
    def test_valid_course_form(self):
        form_data = {
            'name': 'Test Course',
            'description': 'A test course description',
            'image': 'test.jpg'
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_missing_required_fields(self):
        form_data = {'name': 'Test Course'}  # Missing description
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
```

This comprehensive forms documentation provides complete details about all form classes, their usage, validation, security considerations, and integration examples. The documentation includes practical code examples and best practices for working with Django forms in the QuizMate application.
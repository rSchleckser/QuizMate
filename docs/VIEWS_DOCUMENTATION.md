# QuizMate Views Documentation

## Table of Contents

1. [View Overview](#view-overview)
2. [Authentication Views](#authentication-views)
3. [Dashboard Views](#dashboard-views)
4. [Course Management Views](#course-management-views)
5. [Quiz Management Views](#quiz-management-views)
6. [Question Management Views](#question-management-views)
7. [Enrollment Views](#enrollment-views)
8. [Student Views](#student-views)
9. [Authentication & Permissions](#authentication--permissions)
10. [Error Handling](#error-handling)

---

## View Overview

The QuizMate application contains 23 view functions organized into the following categories:

- **Authentication**: User registration, login, logout
- **Dashboards**: Student and instructor dashboards
- **Course Management**: CRUD operations for courses
- **Quiz Management**: CRUD operations for quizzes
- **Question Management**: CRUD operations for questions
- **Enrollment**: Student course enrollment/unenrollment
- **Student Operations**: Quiz taking, progress tracking

---

## Authentication Views

### `home(request)`
**Location**: `courses/views.py:9-10`
**URL**: `/`
**Method**: `GET`
**Authentication**: None required

**Description**: Displays the application home page.

**Parameters**: None

**Returns**: Rendered `courses/home.html` template

**Example Usage**:
```python
def home(request):
    return render(request, 'courses/home.html')
```

---

### `signup(request)`
**Location**: `courses/views.py:12-27`
**URL**: `/signup/`
**Methods**: `GET`, `POST`
**Authentication**: None required

**Description**: User registration for students and instructors.

**GET Parameters**: None

**POST Parameters**:
- `username` (string, required): Unique username
- `password1` (string, required): Password
- `password2` (string, required): Password confirmation
- `user_type` (string, required): Either "student" or "instructor"

**Returns**: 
- `GET`: Registration form
- `POST`: Redirect to appropriate dashboard on success, form with errors on failure

**Logic Flow**:
1. Display registration form on GET
2. Validate form data on POST
3. Create user with appropriate role flags
4. Log in user automatically
5. Redirect to dashboard based on user type

**Example**:
```python
# POST request creates user
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
```

---

### `login_view(request)`
**Location**: `courses/views.py:29-37`
**URL**: `/login/`
**Methods**: `GET`, `POST`
**Authentication**: None required

**Description**: User authentication and session creation.

**GET Parameters**: None

**POST Parameters**:
- `username` (string, required): User's username
- `password` (string, required): User's password

**Returns**:
- `GET`: Login form
- `POST`: Redirect to appropriate dashboard on success, login form on failure

**Example**:
```python
username = request.POST['username']
password = request.POST['password']
user = authenticate(request, username=username, password=password)
if user is not None:
    login(request, user)
    return redirect('student_dashboard' if user.is_student else 'instructor_dashboard')
```

---

### `logout_view(request)`
**Location**: `courses/views.py:39-41`
**URL**: `/logout/`
**Method**: `POST`
**Authentication**: Required

**Description**: End user session and redirect to home.

**Parameters**: None

**Returns**: Redirect to home page

---

## Dashboard Views

### `student_dashboard(request)`
**Location**: `courses/views.py:43-54`
**URL**: `/student/dashboard/`
**Method**: `GET`
**Authentication**: Required (Student only)

**Description**: Display student dashboard with available and enrolled courses.

**Parameters**: None

**Returns**: Student dashboard with context:
- `available_courses`: Courses not enrolled in
- `enrolled_courses`: Current enrollments
- `student`: Current user

**Authentication Check**:
```python
if not request.user.is_authenticated or not request.user.is_student:
    return redirect('login')
```

**Context Data**:
```python
{
    'available_courses': Course.objects.exclude(enrollments__student=request.user),
    'enrolled_courses': Enrollment.objects.filter(student=request.user),
    'student': request.user,
}
```

---

### `instructor_dashboard(request)`
**Location**: `courses/views.py:88-101`
**URL**: `/instructor/dashboard/`
**Method**: `GET`
**Authentication**: Required (Instructor only)

**Description**: Display instructor dashboard with courses and student statistics.

**Parameters**: None

**Returns**: Instructor dashboard with context:
- `courses`: All courses created by instructor
- `total_students`: Count of enrolled students
- `students`: List of students across all courses
- `user_type`: "Instructor"

**Context Calculation**:
```python
courses = Course.objects.filter(instructor=request.user)
total_students = CustomUser.objects.filter(enrollments__course__in=courses).count()
students = CustomUser.objects.filter(enrollments__course__in=courses)
```

---

## Course Management Views

### `course_create(request)`
**Location**: `courses/views.py:104-116`
**URL**: `/instructor/new_course/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Instructor only)

**Description**: Create a new course.

**GET Parameters**: None

**POST Parameters**:
- `name` (string, required, max 100 chars): Course name
- `description` (text, required): Course description
- `image` (string, optional, max 200 chars): Image filename

**Returns**:
- `GET`: Course creation form
- `POST`: Redirect to instructor dashboard on success, form with errors on failure

**Logic**:
```python
if form.is_valid():
    course = form.save(commit=False)
    course.instructor = request.user  # Set current user as instructor
    course.save()
    return redirect('instructor_dashboard')
```

---

### `course_edit(request, pk)`
**Location**: `courses/views.py:119-130`
**URL**: `/instructor/{pk}/edit/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Instructor only)

**Description**: Edit an existing course.

**URL Parameters**:
- `pk` (integer): Course ID

**POST Parameters**: Same as course creation

**Returns**:
- `GET`: Pre-filled course edit form
- `POST`: Redirect to instructor dashboard on success

**Security**: Only the course instructor can edit their courses (enforced by filtering)

---

### `course_delete(request, pk)`
**Location**: `courses/views.py:133-135`
**URL**: `/instructor/{pk}/delete/`
**Method**: `POST`
**Authentication**: Required (Instructor only)

**Description**: Delete a course.

**URL Parameters**:
- `pk` (integer): Course ID to delete

**Returns**: Redirect to instructor dashboard

**Implementation**:
```python
Course.objects.get(id=pk).delete()
return redirect('instructor_dashboard')
```

---

### `course_detail_instructor(request, pk)`
**Location**: `courses/views.py:160-164`
**URL**: `/instructor/course/{pk}/`
**Method**: `GET`
**Authentication**: Required (Instructor only)

**Description**: Detailed view of a course for instructors.

**URL Parameters**:
- `pk` (integer): Course ID

**Returns**: Course detail page with:
- `course`: Course object
- `students`: Enrolled students
- `quizzes`: All quizzes in the course

---

### `course_detail_student(request, pk)`
**Location**: `courses/views.py:243-287`
**URL**: `/student/course/{pk}/`
**Method**: `GET`
**Authentication**: Required (Student only)

**Description**: Detailed view of enrolled course for students with progress tracking.

**URL Parameters**:
- `pk` (integer): Course ID

**Returns**: Course detail page with comprehensive analytics:
- `course`: Course object
- `quizzes`: Available quizzes
- `user_submissions`: Latest quiz submissions
- `number_of_quizzes_taken`: Count of completed quizzes
- `average_percentage`: Average quiz score
- `quizzes_completed_percentage`: Course completion percentage

**Progress Calculation**:
```python
# Calculate completion percentage
quizzes_completed_percentage = (quizzes_taken / quizzes_completed * 100) if quizzes_completed > 0 else 0

# Update enrollment record
enrollment = Enrollment.objects.get(student=request.user, course=course)
enrollment.progress = quizzes_completed_percentage
enrollment.grade = average_percentage
enrollment.save()
```

---

## Quiz Management Views

### `quiz_create(request, pk)`
**Location**: `courses/views.py:172-188`
**URL**: `/instructor/course/{pk}/quiz/create/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Instructor only)

**Description**: Create a new quiz for a course.

**URL Parameters**:
- `pk` (integer): Course ID

**POST Parameters**:
- `title` (string, required, max 100 chars): Quiz title
- `description` (text, required): Quiz description

**Returns**:
- `GET`: Quiz creation form
- `POST`: Redirect to course detail on success

**Logic**:
```python
if form.is_valid():
    quiz = form.save(commit=False)
    quiz.course = course  # Associate with course
    quiz.save()
    return redirect('course_detail_instructor', pk=course.pk)
```

---

### `quiz_detail_instructor(request, pk)`
**Location**: `courses/views.py:167-170`
**URL**: `/quiz/{pk}/`
**Method**: `GET`
**Authentication**: Required (Instructor only)

**Description**: Detailed view of a quiz for instructors.

**URL Parameters**:
- `pk` (integer): Quiz ID

**Returns**: Quiz detail page with:
- `quiz`: Quiz object
- `questions`: All questions in the quiz

---

### `quiz_edit(request, pk)`
**Location**: `courses/views.py:190-201`
**URL**: `/instructor/course/{pk}/quiz/edit/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Instructor only)

**Description**: Edit an existing quiz.

**URL Parameters**:
- `pk` (integer): Quiz ID

**POST Parameters**: Same as quiz creation

**Returns**:
- `GET`: Pre-filled quiz edit form
- `POST`: Redirect to quiz detail on success

---

### `quiz_delete(request, pk, course_pk)`
**Location**: `courses/views.py:203-205`
**URL**: `/instructor/course/{course_pk}/quiz/{pk}/delete/`
**Method**: `POST`
**Authentication**: Required (Instructor only)

**Description**: Delete a quiz.

**URL Parameters**:
- `pk` (integer): Quiz ID
- `course_pk` (integer): Course ID (for redirect)

**Returns**: Redirect to course detail page

---

## Question Management Views

### `question_create(request, pk)`
**Location**: `courses/views.py:208-222`
**URL**: `/quiz/{pk}/question/create/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Instructor only)

**Description**: Add a new question to a quiz.

**URL Parameters**:
- `pk` (integer): Quiz ID

**POST Parameters**:
- `question` (string, required, max 255 chars): Question text
- `option1` (string, required, max 100 chars): First option
- `option2` (string, required, max 100 chars): Second option
- `option3` (string, required, max 100 chars): Third option
- `option4` (string, required, max 100 chars): Fourth option
- `correct_option` (string, required): Correct option number (1-4)

**Returns**:
- `GET`: Question creation form
- `POST`: Redirect to quiz detail on success

**Logic**:
```python
if form.is_valid():
    question = form.save(commit=False)
    question.quiz = quiz  # Associate with quiz
    question.save()
    return redirect('quiz_detail_instructor', pk=quiz.pk)
```

---

### `question_edit(request, pk, quiz_pk)`
**Location**: `courses/views.py:224-235`
**URL**: `/quiz/{quiz_pk}/question/{pk}/edit/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Instructor only)

**Description**: Edit an existing question.

**URL Parameters**:
- `pk` (integer): Question ID
- `quiz_pk` (integer): Quiz ID (for redirect)

**POST Parameters**: Same as question creation

**Returns**:
- `GET`: Pre-filled question edit form
- `POST`: Redirect to quiz detail on success

---

### `question_delete(request, pk, quiz_pk)`
**Location**: `courses/views.py:237-239`
**URL**: `/quiz/{quiz_pk}/question/{pk}/delete/`
**Method**: `POST`
**Authentication**: Required (Instructor only)

**Description**: Delete a question.

**URL Parameters**:
- `pk` (integer): Question ID
- `quiz_pk` (integer): Quiz ID (for redirect)

**Returns**: Redirect to quiz detail page

---

## Enrollment Views

### `course_enrollment(request, pk)`
**Location**: `courses/views.py:140-145`
**URL**: `/enroll/{pk}/`
**Method**: `POST`
**Authentication**: Required (Student only)

**Description**: Enroll student in a course.

**URL Parameters**:
- `pk` (integer): Course ID

**Returns**: Redirect to student dashboard

**Logic**:
```python
course = Course.objects.get(id=pk)
enrollment, created = Enrollment.objects.get_or_create(
    student=request.user, 
    course=course
)
```

**Note**: Uses `get_or_create` to prevent duplicate enrollments.

---

### `course_unenroll(request, pk)`
**Location**: `courses/views.py:147-154`
**URL**: `/unenroll/{pk}/`
**Method**: `POST`
**Authentication**: Required (Student only)

**Description**: Remove student enrollment from a course.

**URL Parameters**:
- `pk` (integer): Course ID

**Returns**: Redirect to student dashboard

**Logic**:
```python
course = Course.objects.get(id=pk)
enrollment = Enrollment.objects.get(student=request.user, course=course)
enrollment.delete()
```

---

## Student Views

### `student_detail(request, student_id)`
**Location**: `courses/views.py:56-69`
**URL**: `/student/{student_id}/`
**Method**: `GET`
**Authentication**: Required (Instructor only)

**Description**: View student performance details (instructor view).

**URL Parameters**:
- `student_id` (integer): Student ID

**Returns**: Student detail page with:
- `student`: Student user object
- `enrollments`: All student enrollments
- `avg_grade`: Average grade across all courses
- `avg_progress`: Average progress across all courses

---

### `student_profile(request, student_id)`
**Location**: `courses/views.py:71-84`
**URL**: `/student/{student_id}/profile`
**Method**: `GET`
**Authentication**: Required (Student only)

**Description**: View student's own profile and performance.

**URL Parameters**:
- `student_id` (integer): Student ID

**Returns**: Student profile page with same context as `student_detail`

---

### `take_quiz(request, course_id, quiz_id)`
**Location**: `courses/views.py:292-329`
**URL**: `/student/course/{course_id}/quiz/{quiz_id}/`
**Methods**: `GET`, `POST`
**Authentication**: Required (Student only)

**Description**: Take a quiz and submit answers.

**URL Parameters**:
- `course_id` (integer): Course ID
- `quiz_id` (integer): Quiz ID

**GET Parameters**: None

**POST Parameters**:
- `question_{question_id}` (string): Selected option for each question

**Returns**:
- `GET`: Quiz taking interface
- `POST`: Quiz results page

**Quiz Processing Logic**:
```python
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

# Create submission record
Submission.objects.create(
    student=request.user, 
    quiz=quiz, 
    score=score, 
    total_questions=total_questions
)
```

**Result Context**:
- `score`: Number of correct answers
- `total_questions`: Total questions in quiz
- `percentage`: Score percentage
- `feedback`: Performance message
- `student_answers`: Detailed answer review

---

### `quiz_result(request, course_id, quiz_id)`
**Location**: `courses/views.py:332-333`
**URL**: `/course/{course_id}/quiz/{quiz_id}/result/`
**Method**: `GET`
**Authentication**: Required (Student only)

**Description**: Display quiz results (currently minimal implementation).

**URL Parameters**:
- `course_id` (integer): Course ID
- `quiz_id` (integer): Quiz ID

**Returns**: Quiz result template

---

## Authentication & Permissions

### Role-Based Access Control

Each view implements specific authentication and authorization checks:

```python
# Student-only views
if not request.user.is_authenticated or not request.user.is_student:
    return redirect('login')

# Instructor-only views  
if not request.user.is_authenticated or not request.user.is_instructor:
    return redirect('login')
```

### Permission Matrix

| View Category | Student Access | Instructor Access | Anonymous Access |
|---------------|----------------|-------------------|------------------|
| Authentication | ❌ | ❌ | ✅ |
| Student Dashboard | ✅ | ❌ | ❌ |
| Instructor Dashboard | ❌ | ✅ | ❌ |
| Course Creation/Edit | ❌ | ✅ | ❌ |
| Quiz Creation/Edit | ❌ | ✅ | ❌ |
| Question Management | ❌ | ✅ | ❌ |
| Enrollment | ✅ | ❌ | ❌ |
| Quiz Taking | ✅ | ❌ | ❌ |
| Student Details | ✅ (own) | ✅ (all) | ❌ |

---

## Error Handling

### Common Error Patterns

1. **Authentication Failures**: Redirect to login page
2. **Permission Denied**: Redirect to appropriate dashboard
3. **Object Not Found**: Django raises `Http404` (not explicitly handled)
4. **Form Validation**: Re-render form with error messages

### Missing Error Handling

The current implementation lacks comprehensive error handling for:
- Non-existent objects (should use `get_object_or_404`)
- Permission checks for object ownership
- CSRF token validation errors
- Database integrity errors

### Recommended Improvements

```python
# Instead of:
course = Course.objects.get(id=pk)

# Use:
from django.shortcuts import get_object_or_404
course = get_object_or_404(Course, id=pk, instructor=request.user)
```

---

## Performance Considerations

### Database Query Optimization

Several views could benefit from query optimization:

```python
# Inefficient (N+1 queries)
enrolled_courses = Enrollment.objects.filter(student=request.user)

# Better (use select_related)
enrolled_courses = Enrollment.objects.select_related('course', 'course__instructor').filter(student=request.user)

# For quiz detail with questions
quiz = Quiz.objects.prefetch_related('questions').get(id=quiz_id)
```

### Caching Opportunities

Consider caching for:
- Course lists on dashboards
- Student progress calculations
- Quiz statistics

---

## Security Considerations

### Current Security Measures

1. **CSRF Protection**: All forms include CSRF tokens
2. **Authentication Required**: Protected views check authentication
3. **Role-Based Access**: Views verify user roles
4. **SQL Injection Protection**: Django ORM prevents SQL injection

### Security Gaps

1. **Object-Level Permissions**: Views don't verify ownership
2. **Rate Limiting**: No protection against rapid submissions
3. **Input Validation**: Limited server-side validation
4. **Session Security**: Default Django session settings

### Recommended Security Enhancements

```python
# Add object-level permission checks
@login_required
@require_http_methods(["GET", "POST"])
def course_edit(request, pk):
    course = get_object_or_404(Course, id=pk, instructor=request.user)
    # ... rest of view logic

# Add rate limiting for quiz submissions
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='1/m', method='POST')
def take_quiz(request, course_id, quiz_id):
    # ... quiz logic
```
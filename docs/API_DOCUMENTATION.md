# QuizMate API Documentation

![QuizMate ERD](../course_images/ERD.png)

## Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Course Management](#course-management)
4. [Quiz Management](#quiz-management)
5. [Question Management](#question-management)
6. [Enrollment Management](#enrollment-management)
7. [Student Dashboard](#student-dashboard)
8. [Instructor Dashboard](#instructor-dashboard)
9. [Error Responses](#error-responses)
10. [Examples](#examples)

## Authentication

All endpoints require proper authentication and role-based access control.

### Authentication Methods
- **Session Authentication**: Django's built-in session authentication
- **User Roles**: `is_student` and `is_instructor` flags determine access levels

### Authentication Headers
```
Cookie: sessionid=<session_id>
```

---

## User Management

### POST `/signup/`
**Description**: Register a new user (student or instructor)

**Authentication**: None required

**Parameters**:
```json
{
    "username": "string (required)",
    "password1": "string (required)",
    "password2": "string (required)",
    "user_type": "student|instructor (required)"
}
```

**Response**: Redirects to appropriate dashboard

**Example**:
```bash
curl -X POST http://localhost:8000/signup/ \
  -d "username=johndoe&password1=securepass123&password2=securepass123&user_type=student"
```

### POST `/login/`
**Description**: Authenticate user and create session

**Authentication**: None required

**Parameters**:
```json
{
    "username": "string (required)",
    "password": "string (required)"
}
```

**Response**: Redirects to appropriate dashboard based on user role

**Example**:
```bash
curl -X POST http://localhost:8000/login/ \
  -d "username=johndoe&password=securepass123"
```

### POST `/logout/`
**Description**: End user session

**Authentication**: Required

**Response**: Redirects to home page

---

## Course Management

### GET `/instructor/dashboard/`
**Description**: Get instructor dashboard with all courses and statistics

**Authentication**: Required (Instructor only)

**Response Data**:
- List of courses created by instructor
- Total enrolled students count
- Student list across all courses

### POST `/instructor/new_course/`
**Description**: Create a new course

**Authentication**: Required (Instructor only)

**Parameters**:
```json
{
    "name": "string (required, max 100 chars)",
    "description": "text (required)",
    "image": "string (optional, max 200 chars)"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/instructor/new_course/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "name=Python Programming&description=Learn Python basics&image=python.jpg"
```

### GET `/instructor/course/{course_id}/`
**Description**: Get detailed view of a specific course for instructor

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `course_id` (integer): ID of the course

**Response Data**:
- Course details
- Enrolled students list
- Associated quizzes

### PUT `/instructor/{course_id}/edit/`
**Description**: Update course details

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `course_id` (integer): ID of the course to edit

**Parameters**: Same as course creation

### DELETE `/instructor/{course_id}/delete/`
**Description**: Delete a course

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `course_id` (integer): ID of the course to delete

**Response**: Redirects to instructor dashboard

---

## Quiz Management

### POST `/instructor/course/{course_id}/quiz/create/`
**Description**: Create a new quiz for a course

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `course_id` (integer): ID of the course

**Parameters**:
```json
{
    "title": "string (required, max 100 chars)",
    "description": "text (required)"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/instructor/course/1/quiz/create/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "title=Python Basics Quiz&description=Test your Python knowledge"
```

### GET `/quiz/{quiz_id}/`
**Description**: Get quiz details for instructor view

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `quiz_id` (integer): ID of the quiz

**Response Data**:
- Quiz details
- All questions in the quiz

### PUT `/instructor/course/{quiz_id}/quiz/edit/`
**Description**: Update quiz details

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `quiz_id` (integer): ID of the quiz to edit

### DELETE `/instructor/course/{course_id}/quiz/{quiz_id}/delete/`
**Description**: Delete a quiz

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `course_id` (integer): ID of the course
- `quiz_id` (integer): ID of the quiz to delete

---

## Question Management

### POST `/quiz/{quiz_id}/question/create/`
**Description**: Add a new question to a quiz

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `quiz_id` (integer): ID of the quiz

**Parameters**:
```json
{
    "question": "string (required, max 255 chars)",
    "option1": "string (required, max 100 chars)",
    "option2": "string (required, max 100 chars)",
    "option3": "string (required, max 100 chars)",
    "option4": "string (required, max 100 chars)",
    "correct_option": "string (required, 1-4)"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/quiz/1/question/create/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "question=What is Python?&option1=A snake&option2=A programming language&option3=A movie&option4=A game&correct_option=2"
```

### PUT `/quiz/{quiz_id}/question/{question_id}/edit/`
**Description**: Update a question

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `quiz_id` (integer): ID of the quiz
- `question_id` (integer): ID of the question to edit

### DELETE `/quiz/{quiz_id}/question/{question_id}/delete/`
**Description**: Delete a question

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `quiz_id` (integer): ID of the quiz
- `question_id` (integer): ID of the question to delete

---

## Enrollment Management

### POST `/enroll/{course_id}/`
**Description**: Enroll student in a course

**Authentication**: Required (Student only)

**URL Parameters**:
- `course_id` (integer): ID of the course to enroll in

**Response**: Redirects to student dashboard

**Example**:
```bash
curl -X POST http://localhost:8000/enroll/1/ \
  -H "Cookie: sessionid=<session_id>"
```

### DELETE `/unenroll/{course_id}/`
**Description**: Remove student enrollment from a course

**Authentication**: Required (Student only)

**URL Parameters**:
- `course_id` (integer): ID of the course to unenroll from

---

## Student Dashboard

### GET `/student/dashboard/`
**Description**: Get student dashboard with available and enrolled courses

**Authentication**: Required (Student only)

**Response Data**:
- Available courses (not enrolled)
- Enrolled courses with progress
- Student statistics

### GET `/student/course/{course_id}/`
**Description**: Get detailed view of enrolled course for student

**Authentication**: Required (Student only)

**URL Parameters**:
- `course_id` (integer): ID of the enrolled course

**Response Data**:
- Course details
- Available quizzes
- Student progress and grades
- Quiz submission history

### POST `/student/course/{course_id}/quiz/{quiz_id}/`
**Description**: Take a quiz and submit answers

**Authentication**: Required (Student only)

**URL Parameters**:
- `course_id` (integer): ID of the course
- `quiz_id` (integer): ID of the quiz

**Parameters**:
```json
{
    "question_{question_id}": "selected_option_number"
}
```

**Response Data**:
- Quiz results
- Score and percentage
- Correct/incorrect answers
- Feedback

**Example**:
```bash
curl -X POST http://localhost:8000/student/course/1/quiz/1/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "question_1=2&question_2=1&question_3=4"
```

---

## Instructor Dashboard

### GET `/instructor/dashboard/`
**Description**: Get instructor dashboard with courses and student statistics

**Authentication**: Required (Instructor only)

**Response Data**:
- All courses created by instructor
- Total student count
- Student performance overview

### GET `/student/{student_id}/`
**Description**: Get detailed student performance (instructor view)

**Authentication**: Required (Instructor only)

**URL Parameters**:
- `student_id` (integer): ID of the student

**Response Data**:
- Student information
- All enrollments
- Average grades and progress

---

## Error Responses

### 401 Unauthorized
```json
{
    "error": "Authentication required",
    "redirect": "/login/"
}
```

### 403 Forbidden
```json
{
    "error": "Insufficient permissions",
    "message": "This action requires instructor privileges"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found",
    "message": "The requested course/quiz/question does not exist"
}
```

### 400 Bad Request
```json
{
    "error": "Invalid data",
    "fields": {
        "name": ["This field is required"],
        "description": ["This field cannot be blank"]
    }
}
```

---

## Examples

### Complete Course Creation Workflow

1. **Create Course**:
```bash
curl -X POST http://localhost:8000/instructor/new_course/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "name=Advanced Python&description=Advanced Python concepts&image=python.jpg"
```

2. **Create Quiz**:
```bash
curl -X POST http://localhost:8000/instructor/course/1/quiz/create/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "title=Python OOP Quiz&description=Object-Oriented Programming concepts"
```

3. **Add Questions**:
```bash
curl -X POST http://localhost:8000/quiz/1/question/create/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "question=What is encapsulation?&option1=Hiding data&option2=Inheritance&option3=Polymorphism&option4=Abstraction&correct_option=1"
```

### Student Quiz Taking Workflow

1. **Enroll in Course**:
```bash
curl -X POST http://localhost:8000/enroll/1/ \
  -H "Cookie: sessionid=<session_id>"
```

2. **Take Quiz**:
```bash
curl -X POST http://localhost:8000/student/course/1/quiz/1/ \
  -H "Cookie: sessionid=<session_id>" \
  -d "question_1=1&question_2=3"
```

### Authentication Flow

1. **Register**:
```bash
curl -X POST http://localhost:8000/signup/ \
  -d "username=instructor1&password1=securepass123&password2=securepass123&user_type=instructor"
```

2. **Login**:
```bash
curl -X POST http://localhost:8000/login/ \
  -d "username=instructor1&password=securepass123"
```

3. **Use authenticated endpoints with session cookie**

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use:
- Authentication endpoints: 5 requests per minute
- Quiz submission: 1 request per quiz per student
- Course creation: 10 requests per hour per instructor

## Security Considerations

- All forms include CSRF protection
- User input is validated and sanitized
- SQL injection protection via Django ORM
- Session-based authentication with secure cookies
- Role-based access control enforced at view level
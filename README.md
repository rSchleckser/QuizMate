# QuizMate - Instructor and Student Dashboard

Welcome to QuizMate, a comprehensive platform for managing courses, quizzes, and students. This project provides an intuitive dashboard for instructors to create and manage courses and quizzes, view student performance, and much more.

## Table of Contents
1. [Project Description](#project-description)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
6. [Wireframes](#wireframes)
7. [Trello Board](#trello-board)

## Project Description

QuizMate is designed to simplify the process of course and quiz management for instructors and provide students with a seamless experience for course enrollment and quiz submissions. Instructors can create courses and quizzes, view student enrollments and quiz submissions, and analyze course and quiz performance, while students can browse available courses, enroll, take quizzes, and monitor their progress.

### Features

- **Instructor Dashboard**: Create and manage courses and quizzes, view enrolled students and quiz submissions, and analyze course and quiz performance.
- **Student Dashboard**: Browse and enroll in courses, view enrolled courses, take quizzes, and track progress.
- **Authentication**: Secure login and registration for both instructors and students.
- **Course and Quiz Management**: Create, edit, and delete courses and quizzes, upload images for courses and quizzes.
- **Analytics**: View detailed analytics on student performance and course effectiveness.

## Technologies Used

- **Backend**:
  - Django
  - PostgreSQL

- **Frontend**:
  - HTML
  - CSS
  - Bootstrap

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/quizmate.git
    cd quizmate
    ```

2. **Create a virtual environment and activate it**:
    - **On macOS and Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    - **On Windows**:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

- Visit `http://127.0.0.1:8000` in your browser.
- Log in with your superuser credentials or create a new instructor/student account.
- Navigate to the instructor or student dashboard to start managing or enrolling in courses and quizzes.

## Entity Relationship Diagram (ERD)

![ERD](/course_images/ERD.png)

### ERD Description

- **User**:
  - Fields: `username`, `password`, `email`, `is_instructor`, `is_student`
  - Relationships: One-to-Many with Course (if instructor), Many-to-Many with Course (if student through Enrollment), One-to-Many with Quiz (if instructor), Many-to-Many with Quiz (if student through Submission)

- **Course**:
  - Fields: `name`, `description`, `instructor (Foreign Key)`, `image`
  - Relationships: Many-to-One with User (instructor), Many-to-Many with User (student through Enrollment), One-to-Many with Quiz

- **Quiz**:
  - Fields: `title`, `course (Foreign Key)`, `created_at`
  - Relationships: Many-to-One with Course, One-to-Many with Question, One-to-Many with Submission

- **Question**:
  - Fields: `text`, `quiz (Foreign Key)`, `created_at`
  - Relationships: Many-to-One with Quiz

- **Submission**:
  - Fields: `student (Foreign Key)`, `quiz (Foreign Key)`, `submitted_at`
  - Relationships: Many-to-One with User (student), Many-to-One with Quiz

- **Enrollment**:
  - Fields: `user (Foreign Key)`, `course (Foreign Key)`
  - Relationships: Many-to-Many linking User and Course

## Wireframes

### Instructor Dashboard Wireframe

![Instructor Dashboard Wireframe](/course_images/instructor_wireframe.png)

### Student Dashboard Wireframe

![Student Dashboard Wireframe](/course_images/student_wireframe.png)

## Trello Board

Visit our [Trello Board](https://trello.com/invite/b/66b2ee72447f4f92f48b2e02/ATTI9eedb0b653f106bf7ad903831173cfcbF986AB3B/quizmate-development) to see the development of QuizMate.

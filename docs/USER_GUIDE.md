# QuizMate User Guide

![QuizMate Instructor Dashboard](../course_images/instructor_wireframe.png)
![QuizMate Student Dashboard](../course_images/student_wireframe.png)

## Table of Contents

1. [Getting Started](#getting-started)
2. [Account Registration & Login](#account-registration--login)
3. [Instructor Guide](#instructor-guide)
4. [Student Guide](#student-guide)
5. [Features Overview](#features-overview)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## Getting Started

### System Requirements

- **Web Browser**: Chrome 70+, Firefox 65+, Safari 12+, Edge 79+
- **Internet Connection**: Required for all functionality
- **JavaScript**: Must be enabled
- **Cookies**: Must be enabled for authentication

### Accessing QuizMate

1. **Live Application**: Visit [https://courses-service-1f17.onrender.com](https://courses-service-1f17.onrender.com)
2. **Local Development**: Visit `http://127.0.0.1:8000` (if running locally)

### User Roles

QuizMate supports two types of users:

- **Students**: Can enroll in courses, take quizzes, and track progress
- **Instructors**: Can create courses, design quizzes, and monitor student performance

---

## Account Registration & Login

### Creating an Account

1. **Navigate to Registration**
   - Click "Sign Up" from the home page
   - Or visit `/signup/` directly

2. **Fill Registration Form**
   ```
   Username: [Choose a unique username]
   Password: [Create a strong password]
   Confirm Password: [Re-enter your password]
   User Type: ○ I am a student  ○ I am an instructor
   ```

3. **Complete Registration**
   - Click "Sign Up" button
   - You'll be automatically logged in and redirected to your dashboard

### Logging In

1. **Access Login Page**
   - Click "Login" from the home page
   - Or visit `/login/` directly

2. **Enter Credentials**
   ```
   Username: [Your username]
   Password: [Your password]
   ```

3. **Access Dashboard**
   - Click "Login" button
   - You'll be redirected to your role-specific dashboard

### Logging Out

- Click "Logout" from any page when logged in
- You'll be redirected to the home page

---

## Instructor Guide

### Dashboard Overview

The instructor dashboard provides:
- **Course Management**: View all your courses
- **Student Statistics**: Total enrolled students across all courses
- **Quick Actions**: Create new courses, view student details

### Creating Your First Course

#### Step 1: Access Course Creation
- From your dashboard, click "Create New Course"
- Or navigate to `/instructor/new_course/`

#### Step 2: Fill Course Details
```
Course Name: [e.g., "Python Programming Fundamentals"]
Description: [Detailed course description]
Course Image: [Optional - filename like "python.jpg"]
```

#### Step 3: Save Course
- Click "Save Course"
- You'll be redirected to your dashboard with the new course listed

### Managing Courses

#### Viewing Course Details
1. Click on any course from your dashboard
2. View enrolled students and course quizzes
3. Access options to edit or delete the course

#### Editing a Course
1. From course detail page, click "Edit Course"
2. Modify course information
3. Click "Update Course" to save changes

#### Deleting a Course
1. From course detail page, click "Delete Course"
2. **Warning**: This permanently removes the course and all associated quizzes and student progress

### Creating Quizzes

#### Step 1: Access Quiz Creation
1. Go to your course detail page
2. Click "Create New Quiz"
3. Or use the "Add Quiz" button

#### Step 2: Set Quiz Details
```
Quiz Title: [e.g., "Python Basics Assessment"]
Description: [What the quiz covers]
```

#### Step 3: Add Questions
1. After creating the quiz, click "Add Question"
2. Fill in question details:
   ```
   Question: [Your question text]
   Option 1: [First answer choice]
   Option 2: [Second answer choice]
   Option 3: [Third answer choice]
   Option 4: [Fourth answer choice]
   Correct Option: [Enter 1, 2, 3, or 4]
   ```

#### Step 4: Review and Publish
- Add multiple questions as needed
- Review all questions for accuracy
- Quiz is immediately available to enrolled students

### Managing Questions

#### Adding Questions
- From quiz detail page, click "Add Question"
- Fill in all required fields
- Ensure the correct option number matches your intended answer

#### Editing Questions
1. From quiz detail page, click "Edit" next to any question
2. Modify question content or answers
3. Click "Save Question"

#### Deleting Questions
- Click "Delete" next to any question
- **Warning**: This permanently removes the question

### Monitoring Student Progress

#### Viewing Enrolled Students
1. Go to course detail page
2. View list of enrolled students
3. Click on any student name to see detailed performance

#### Student Performance Details
- **Average Grade**: Student's average quiz score
- **Progress**: Percentage of course completion
- **Individual Quiz Results**: Scores for each quiz attempt

### Best Practices for Instructors

#### Course Creation
- Write clear, descriptive course names
- Provide comprehensive course descriptions
- Use relevant course images when available

#### Quiz Design
- Start with easier questions to build confidence
- Include 5-10 questions per quiz for optimal engagement
- Write clear, unambiguous questions
- Ensure answer options are distinct and reasonable

#### Question Writing
- Use simple, direct language
- Avoid trick questions
- Include one clearly correct answer
- Make incorrect options plausible but wrong

---

## Student Guide

### Dashboard Overview

The student dashboard shows:
- **Available Courses**: Courses you can enroll in
- **Enrolled Courses**: Courses you're currently taking
- **Progress Summary**: Your performance across all courses

### Enrolling in Courses

#### Step 1: Browse Available Courses
- View course list on your dashboard
- Read course descriptions to understand content
- Check instructor information

#### Step 2: Enroll in Course
1. Click "Enroll" button next to desired course
2. You'll be automatically enrolled
3. Course moves to "Enrolled Courses" section

#### Step 3: Access Course Content
- Click on enrolled course to view details
- See available quizzes and your progress

### Taking Quizzes

#### Step 1: Access Quiz
1. Go to your enrolled course page
2. Click on any available quiz
3. Review quiz description and requirements

#### Step 2: Complete Quiz
1. Read each question carefully
2. Select your answer by clicking the radio button
3. You can change answers before submitting
4. Click "Submit Quiz" when ready

#### Step 3: Review Results
- View your score immediately after submission
- See correct answers and explanations
- Check which questions you got right/wrong
- Note your percentage score

### Tracking Your Progress

#### Course Progress
- **Overall Progress**: Percentage of quizzes completed
- **Average Grade**: Your average score across all quizzes
- **Individual Quiz Scores**: Detailed breakdown of each attempt

#### Viewing Your Profile
1. Click on your name or "Profile" link
2. View statistics across all enrolled courses:
   - Average grade across all courses
   - Overall progress percentage
   - Course-by-course breakdown

### Managing Your Enrollments

#### Unenrolling from Courses
1. Go to course detail page
2. Click "Unenroll" button
3. **Warning**: This removes all your progress data

#### Retaking Quizzes
- You can retake quizzes multiple times
- Only your latest score is used for grade calculation
- Previous attempts are stored for reference

### Best Practices for Students

#### Before Taking Quizzes
- Review course materials thoroughly
- Take notes on key concepts
- Understand the quiz format and time requirements

#### During Quizzes
- Read questions carefully and completely
- Eliminate obviously wrong answers first
- Don't rush - take time to think through each question
- Review your answers before submitting

#### After Quizzes
- Review incorrect answers to understand mistakes
- Note areas that need more study
- Retake quizzes if needed to improve understanding

---

## Features Overview

### Authentication System
- **Secure Registration**: Password validation and user role selection
- **Session Management**: Automatic login/logout with session security
- **Role-Based Access**: Different interfaces for students and instructors

### Course Management
- **CRUD Operations**: Create, read, update, delete courses
- **Student Enrollment**: Easy enrollment/unenrollment process
- **Progress Tracking**: Automatic calculation of student progress

### Quiz System
- **Multiple Choice Questions**: Support for 4-option questions
- **Immediate Feedback**: Instant results after quiz submission
- **Multiple Attempts**: Students can retake quizzes
- **Detailed Results**: Show correct/incorrect answers

### Analytics & Reporting
- **Student Performance**: Individual and aggregate statistics
- **Course Analytics**: Enrollment numbers and completion rates
- **Progress Monitoring**: Real-time progress updates

### User Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Bootstrap Styling**: Modern, consistent interface
- **Intuitive Navigation**: Clear menu structure and breadcrumbs

---

## Troubleshooting

### Common Issues

#### Cannot Log In
**Problem**: Username/password not working
**Solutions**:
- Verify username and password are correct
- Check if Caps Lock is on
- Clear browser cache and cookies
- Try a different browser

#### Course Not Appearing
**Problem**: Created course doesn't show up
**Solutions**:
- Refresh the page
- Check if you're logged in as an instructor
- Verify course was saved successfully

#### Quiz Submission Failed
**Problem**: Quiz won't submit or shows error
**Solutions**:
- Ensure all questions are answered
- Check internet connection
- Try refreshing the page and resubmitting
- Clear browser cache

#### Permission Errors
**Problem**: "Access denied" or similar messages
**Solutions**:
- Verify you're logged in with correct account type
- Check if you have permission for the action
- Log out and log back in

### Browser Issues

#### JavaScript Disabled
- Enable JavaScript in browser settings
- Some features may not work without JavaScript

#### Cookies Disabled
- Enable cookies for the QuizMate domain
- Authentication requires cookies to be enabled

#### Cache Problems
- Clear browser cache and cookies
- Try incognito/private browsing mode
- Hard refresh with Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

### Getting Help

If you continue experiencing issues:
1. Check the FAQ section below
2. Try using a different browser
3. Contact system administrator
4. Report bugs through the issue tracking system

---

## Best Practices

### For Instructors

#### Course Design
- **Clear Objectives**: Define what students should learn
- **Logical Structure**: Organize content from basic to advanced
- **Regular Updates**: Keep course content current and relevant

#### Quiz Creation
- **Balanced Difficulty**: Mix easy, medium, and hard questions
- **Clear Instructions**: Provide clear quiz instructions
- **Immediate Feedback**: Use quiz results to guide instruction

#### Student Engagement
- **Regular Monitoring**: Check student progress frequently
- **Timely Feedback**: Respond to student performance quickly
- **Encouragement**: Provide positive reinforcement for improvement

### For Students

#### Effective Learning
- **Regular Study**: Don't cram before quizzes
- **Active Participation**: Engage with course content actively
- **Ask Questions**: Seek help when concepts are unclear

#### Quiz Strategies
- **Preparation**: Review materials before taking quizzes
- **Time Management**: Don't spend too long on single questions
- **Learning from Mistakes**: Use incorrect answers as learning opportunities

---

## FAQ

### General Questions

**Q: Is QuizMate free to use?**
A: Yes, QuizMate is free for all users.

**Q: Can I change my account type after registration?**
A: No, you need to create a new account with the desired role.

**Q: Is my data secure?**
A: Yes, QuizMate uses industry-standard security practices including password hashing and CSRF protection.

### For Students

**Q: Can I see my quiz answers after submission?**
A: Yes, you can review your answers and see which ones were correct immediately after submission.

**Q: How many times can I retake a quiz?**
A: There's no limit on quiz attempts. Your latest score is used for grade calculation.

**Q: Can I unenroll from a course?**
A: Yes, but this will permanently delete your progress data for that course.

**Q: How is my grade calculated?**
A: Your grade is the average percentage across all your latest quiz attempts in the course.

### For Instructors

**Q: Can I edit questions after students have taken the quiz?**
A: Yes, but changes won't affect previously submitted answers.

**Q: Can I see individual student quiz responses?**
A: Currently, you can see student scores but not individual answer choices.

**Q: Is there a limit on courses or quizzes I can create?**
A: No, there are no limits on the number of courses or quizzes you can create.

**Q: Can I download student data?**
A: Currently, there's no export feature, but you can view all data through the web interface.

### Technical Questions

**Q: What browsers are supported?**
A: QuizMate works best on modern browsers: Chrome 70+, Firefox 65+, Safari 12+, Edge 79+.

**Q: Does QuizMate work on mobile devices?**
A: Yes, the interface is responsive and works on tablets and smartphones.

**Q: Can I integrate QuizMate with other systems?**
A: QuizMate doesn't currently have API endpoints for external integration.

**Q: Is there an offline mode?**
A: No, QuizMate requires an internet connection to function.

---

## Quick Reference

### URL Patterns
- **Home**: `/`
- **Login**: `/login/`
- **Register**: `/signup/`
- **Student Dashboard**: `/student/dashboard/`
- **Instructor Dashboard**: `/instructor/dashboard/`
- **Create Course**: `/instructor/new_course/`
- **Take Quiz**: `/student/course/{course_id}/quiz/{quiz_id}/`

### Keyboard Shortcuts
- **Tab**: Navigate between form fields
- **Enter**: Submit forms (when focus is on submit button)
- **Escape**: Close modal dialogs (if implemented)

### User Roles Summary

| Feature | Student | Instructor |
|---------|---------|------------|
| View Courses | Available only | Own courses |
| Enroll in Courses | ✅ | ❌ |
| Create Courses | ❌ | ✅ |
| Take Quizzes | ✅ | ❌ |
| Create Quizzes | ❌ | ✅ |
| View All Students | ❌ | ✅ |
| View Own Progress | ✅ | ❌ |

This comprehensive user guide provides step-by-step instructions for both students and instructors, covering all major features and common scenarios in QuizMate.
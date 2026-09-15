from django.test import TestCase
from django.urls import reverse

from .models import CustomUser, Course, Enrollment, Quiz, Question, Submission


def make_instructor(username='instructor'):
    return CustomUser.objects.create_user(username=username, password='pass1234', is_instructor=True)


def make_student(username='student'):
    return CustomUser.objects.create_user(username=username, password='pass1234', is_student=True)


class OwnershipTests(TestCase):
    def setUp(self):
        self.owner = make_instructor('owner')
        self.other = make_instructor('other')
        self.course = Course.objects.create(name='Course', description='desc', instructor=self.owner)
        self.quiz = Quiz.objects.create(course=self.course, title='Quiz', description='desc')
        self.question = Question.objects.create(
            quiz=self.quiz, question='Q?', option1='a', option2='b', option3='c', option4='d',
            correct_option=1,
        )

    def test_non_owner_cannot_edit_course(self):
        self.client.login(username='other', password='pass1234')
        response = self.client.get(reverse('course_edit', args=[self.course.pk]))
        self.assertEqual(response.status_code, 403)

    def test_non_owner_cannot_delete_course(self):
        self.client.login(username='other', password='pass1234')
        response = self.client.post(reverse('course_delete', args=[self.course.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())

    def test_non_owner_cannot_delete_quiz(self):
        self.client.login(username='other', password='pass1234')
        response = self.client.post(reverse('quiz_delete', args=[self.course.pk, self.quiz.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Quiz.objects.filter(pk=self.quiz.pk).exists())

    def test_non_owner_cannot_delete_question(self):
        self.client.login(username='other', password='pass1234')
        response = self.client.post(reverse('question_delete', args=[self.quiz.pk, self.question.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Question.objects.filter(pk=self.question.pk).exists())

    def test_owner_can_edit_course(self):
        self.client.login(username='owner', password='pass1234')
        response = self.client.get(reverse('course_edit', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)


class AuthRequiredTests(TestCase):
    def setUp(self):
        self.instructor = make_instructor()
        self.student = make_student()
        self.course = Course.objects.create(name='Course', description='desc', instructor=self.instructor)
        self.quiz = Quiz.objects.create(course=self.course, title='Quiz', description='desc')

    def test_anonymous_redirected_from_instructor_dashboard(self):
        response = self.client.get(reverse('instructor_dashboard'))
        self.assertRedirects(response, reverse('login'))

    def test_student_redirected_from_instructor_only_view(self):
        self.client.login(username='student', password='pass1234')
        response = self.client.get(reverse('course_create'))
        self.assertRedirects(response, reverse('login'))

    def test_anonymous_redirected_from_take_quiz(self):
        response = self.client.get(reverse('take_quiz', args=[self.course.pk, self.quiz.pk]))
        self.assertRedirects(response, reverse('login'))

    def test_instructor_redirected_from_student_only_view(self):
        self.client.login(username='instructor', password='pass1234')
        response = self.client.get(reverse('student_dashboard'))
        self.assertRedirects(response, reverse('login'))


class StudentProfileTests(TestCase):
    def setUp(self):
        self.student = make_student('alice')
        self.other_student = make_student('bob')

    def test_student_can_view_own_profile(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('student_profile', args=[self.student.pk]))
        self.assertEqual(response.status_code, 200)

    def test_student_cannot_view_others_profile(self):
        self.client.login(username='alice', password='pass1234')
        response = self.client.get(reverse('student_profile', args=[self.other_student.pk]))
        self.assertEqual(response.status_code, 403)


class NotFoundTests(TestCase):
    def setUp(self):
        self.instructor = make_instructor()

    def test_missing_course_returns_404(self):
        self.client.login(username='instructor', password='pass1234')
        response = self.client.get(reverse('course_edit', args=[999999]))
        self.assertEqual(response.status_code, 404)


class QuizScoringTests(TestCase):
    def setUp(self):
        self.instructor = make_instructor()
        self.student = make_student()
        self.course = Course.objects.create(name='Course', description='desc', instructor=self.instructor)
        self.quiz = Quiz.objects.create(course=self.course, title='Quiz', description='desc')
        self.question = Question.objects.create(
            quiz=self.quiz, question='2+2?', option1='3', option2='4', option3='5', option4='6',
            correct_option=2,
        )
        Enrollment.objects.create(student=self.student, course=self.course)

    def test_is_correct_matches_on_int_option(self):
        self.assertTrue(self.question.is_correct('2'))
        self.assertFalse(self.question.is_correct('1'))

    def test_is_correct_handles_missing_answer(self):
        self.assertFalse(self.question.is_correct(None))

    def test_get_correct_answer(self):
        self.assertEqual(self.question.get_correct_answer(), '4')

    def test_take_quiz_scores_submission(self):
        self.client.login(username='student', password='pass1234')
        response = self.client.post(
            reverse('take_quiz', args=[self.course.pk, self.quiz.pk]),
            {f'question_{self.question.pk}': '2'},
        )
        self.assertEqual(response.status_code, 200)
        submission = Submission.objects.get(student=self.student, quiz=self.quiz)
        self.assertEqual(submission.score, 1)
        self.assertEqual(submission.total_questions, 1)


class ProgressUpdateTests(TestCase):
    def setUp(self):
        self.instructor = make_instructor()
        self.student = make_student()
        self.course = Course.objects.create(name='Course', description='desc', instructor=self.instructor)
        self.quiz = Quiz.objects.create(course=self.course, title='Quiz', description='desc')
        self.question = Question.objects.create(
            quiz=self.quiz, question='2+2?', option1='3', option2='4', option3='5', option4='6',
            correct_option=2,
        )
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)

    def test_viewing_course_detail_does_not_mutate_enrollment(self):
        self.client.login(username='student', password='pass1234')
        self.client.get(reverse('course_detail_student', args=[self.course.pk]))
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.progress, 0.0)
        self.assertEqual(self.enrollment.grade, 0.0)

    def test_submitting_quiz_updates_enrollment_progress(self):
        self.client.login(username='student', password='pass1234')
        self.client.post(
            reverse('take_quiz', args=[self.course.pk, self.quiz.pk]),
            {f'question_{self.question.pk}': '2'},
        )
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.progress, 100.0)
        self.assertEqual(self.enrollment.grade, 100.0)

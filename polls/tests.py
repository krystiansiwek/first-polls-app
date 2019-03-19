import datetime

from django.test import TestCase
from django.test import Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.forms import User

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):

        time = timezone.now() - datetime.timedelta(hours=23, minutes=45)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls available')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question>']
        )

    def test_future_question(self):
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls available')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_future_and_past_question(self):
        create_question(question_text='Future question', days=30)
        create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question>']
        )

    def test_two_past_questions(self):
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text='Past question 2', days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question 1>', '<Question: Past question 2>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:details', args=[future_question.id]))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question', days=-20)
        response = self.client.get(reverse('polls:details', args=[past_question.id]))
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question', days=50)
        response = self.client.get(reverse('polls:results', args=[future_question.id]))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question', days=-25)
        response = self.client.get(reverse('polls:results', args=[past_question.id]))
        self.assertContains(response, past_question.question_text)


class NewPollViewTests(TestCase):
    def test_new_poll_not_logged_in(self):
        response = self.client.get(reverse('polls:new_poll'))
        self.assertRedirects(response, '/login/?next=/polls/new/', 302)

    def test_new_poll_logged_in(self):
        user = User.objects.create_user('testuser')
        self.client.force_login(user)
        response = self.client.get(reverse('polls:new_poll'))
        self.assertEqual(response.status_code, 200)

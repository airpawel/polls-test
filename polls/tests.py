from django.core.urlresolvers import reverse
from django.test import TestCase

import datetime
from django.utils import timezone
from .models import Question


def create_question(question_text,days=0,minutes=0):
    try:
        time = timezone.now()+timezone.timedelta(days=days)+timezone.timedelta(minutes=minutes)
        question = Question.objects.create(question_text=question_text,pub_date=time)
    except:
        print('sth went wrong!\n')
    return question

def create_question_with_choices(question_text,choices=["choice 1","choice 2"],days=0,minutes=0,):
    try:
        time = timezone.now() + timezone.timedelta(days=days) + timezone.timedelta(minutes=minutes)
        question = Question.objects.create(question_text=question_text, pub_date=time)
        question.choice_set.create(choice_text=choices[0], votes=1)
        question.choice_set.create(choice_text=choices[1], votes=1)
    except:
        print('sth went wrong!\n')
    return question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently sholud return False for questions whose
        pub_date is in the future
        :return:
        """
        time =timezone.now() + timezone.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


class QuestionIndexTests(TestCase):

    def test_index_view_with_no_questions(self):

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_index_view_with_only_past_question_with_choices(self):

        question = create_question_with_choices(question_text="Question from Past!",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Question from Past!>']
                                )

    def test_index_view_with_only_future_question(self):

        question = create_question(question_text="Question from Future!",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_index_view_with_future_question_with_choices_and_past_question_with_choices(self):

        future_question = create_question_with_choices(question_text="Question from Future!", days=  30)
        past_question   = create_question_with_choices(question_text="Question from Past!",   days= -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Question from Past!>'] )


    def test_index_view_with_two_past_questions_with_choices(self):
        """
        the number of days which here equals 30 and 9
        does not matter, what matters here is only the sign of number of the days
        """
        past_question_1 = create_question_with_choices(question_text="Question from Past no. 1!", days=-30)
        past_question_2 = create_question_with_choices(question_text="Question from Past no. 2!", days=-9)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Question from Past no. 2!>',
                                  '<Question: Question from Past no. 1!>']
                                )

class QuestionIndexDetailTests(TestCase):

    def test_detail_view_with_a_future_question(self):

        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):

        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.context['question'].question_text,
                                 past_question.question_text
                                 )

class QuestionIndexResultsTests(TestCase):

    def test_results_view_with_a_future_question(self):

        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_results_view_with_a_past_question(self):

        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        # double check of generated response
        self.assertContains(response,past_question.question_text)
        self.assertEqual(response.context['question'].question_text,
                                 past_question.question_text

                         )






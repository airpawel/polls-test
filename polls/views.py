#-*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render, loader, get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import Question, Choice
from django.http import HttpResponse, Http404, HttpResponseRedirect


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        question_with_answers = []
        past_or_equal_question = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        for q in past_or_equal_question:
            if q.choice_set.all():
                question_with_answers.append(q)
        return question_with_answers[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn`t select a choice!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))







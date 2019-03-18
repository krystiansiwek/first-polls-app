from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Choice
from .forms import CreateQuestionView, AddChoiceFormset


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


@login_required
def delete_poll(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        if request.POST.get('delete') and request.user == question.author:
            messages.success(request, 'Poll deleted successfully')
            question.delete()
            return redirect('polls:index')
        else:
            return render(request,
                          'polls/details.html',
                          {'question': question,
                           'error_message': 'You don\'t have permission to do that'})


@login_required
def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,
                      'polls/details.html',
                      {'poll': question,
                       'error_message': 'You didn\'t select any choice. '})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', pk=pk)


@login_required
def new_poll(request):
    if request.method == 'POST':
        new_question_form = CreateQuestionView(request.POST)
        choice_form = AddChoiceFormset(request.POST, request.FILES)

        if new_question_form.is_valid() and choice_form.is_valid():
            question = new_question_form.save(commit=False)
            question.author = request.user
            question.save()

            for form in choice_form:
                if form.cleaned_data.get('choice_text'):
                    choice = form.save(commit=False)
                    choice.question = question
                    choice.save()
            messages.success(request, f'Poll added!')
            return redirect('polls:index')
    else:
        new_question_form = CreateQuestionView()
        choice_form = AddChoiceFormset(queryset=Choice.objects.none(),)

    context = {
        'new_question_form': new_question_form,
        'choice_form': choice_form,
    }
    return render(request,
                  'polls/new_poll.html',
                  context)

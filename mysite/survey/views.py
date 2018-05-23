from django.shortcuts import render, get_object_or_404
from survey.models import Question, Choice, UserResponse
from django import urls
from django.http import HttpResponse, HttpResponseRedirect
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import ColumnChart


def index(request):
    template_name = 'survey/index.html'
    questions = Question.objects.all()
    return render(request, template_name, {'questions': questions})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    userResponse = UserResponse()
    userResponse.question = question
    return render(request, 'survey/detail.html', {'resp': userResponse})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = list(question.choice_set.all())

    data = [['Choice', 'Votes']]
    for choice in choices:
        data.append([choice.choice_text, choice.votes])
    data_source = SimpleDataSource(data=data)
    
    chart = ColumnChart(data_source)
    context = {'question' : question, 'chart': chart}
    return render(request, 'survey/results.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        username = request.POST['username']
        if question.question_type == 'radio':
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        else:
            answer_text = request.POST['answer']
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'survey/index.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.question_type == 'radio':
            answer = selected_choice.choice_text
            selected_choice.votes += 1
            selected_choice.save(update_fields=["votes"])
            redirect_url = urls.reverse('survey:results', args=(question_id,))
        else:
            answer = answer_text
            redirect_url = urls.reverse('survey:index')

        UserResponse.objects.create(
            user=username,
            answer=answer,
            question=question,
        )
        
        return HttpResponseRedirect(redirect_url)
from django.shortcuts import render, get_object_or_404
from survey.models import Question, Choice, UserResponse
from django import urls
from django.http import HttpResponse, HttpResponseRedirect


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
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        username = request.POST['username']
        if question.question_type == 'radio':
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        else:
            answer = request.POST['answer']
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'survey/index.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.question_type == 'radio':
            UserResponse.objects.create(
                user=username,
                answer=selected_choice.choice_text,
                question=question,
            )
            selected_choice.votes += 1
            selected_choice.save(update_fields=["votes"])
        else:
            UserResponse.objects.create(
                user=username,
                answer=answer,
                question=question,
            )
        redirect_url = urls.reverse('survey:index')
        return HttpResponseRedirect(redirect_url)
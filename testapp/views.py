# coding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template import loader
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'testapp/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):

        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'testapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name ='testapp/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 发生choice未找到异常时，重新返回表单页面，并给出提示信息
        return render(request, 'testapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理数据后，自动跳转到结果页面，防止用户连续多次提交。
        return HttpResponseRedirect(reverse('testapp:results', args=(question.id,)))
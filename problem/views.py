'''
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from users.models import User
from problem.models import Problem, Tag, Testcase
from problem.forms import ProblemForm
from general_tools import log

import os
import json

logger = log.get_logger()

# Create your views here.
def problem(request):
    a = {'name': 'my_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    b = {'name': 'all_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    return render(request, 'problem/panel.html', {'my_problem':[a,a,a], 'all_problem':[a,a,a,b,b,b]})

def volume(request):
    problem_id=[]
    if Problem.objects.count() != 0:
        problems = Problem.objects.latest('id')
        volume_number = (problems.id - 1) // 100
        for i in range(1,volume_number + 2):
            start_id = ((i - 1) * 100 + 1)
            if problems.id < i * 100:
                end_id = problems.id
            else:
                end_id = i * 100
            problem_id.append(str(start_id) + ' ~ ' + str(end_id))

    return render(request, 'problem/category.html', {'problem_id':problem_id})

def detail(request, pid):
    print pid
    user = request.user
    try:
        problem = Problem.objects.get(pk=pid)
    except Problem.DoesNotExist:
        logger.warning('problem %s not found' % (pid))
        raise Http404('problem %s does not exist' % (pid))
    testcase = Testcase.objects.filter(problem=problem)
    tag = problem.tags.all()
    return render(request, 'problem/detail.html',
                  {'problem': problem, 'tag': tag, 'testcase': testcase})

def edit(request, pid):
    return render(request, 'problem/edit.html')

def new(request):
    if not request.user.has_subjudge_auth():
        raise PermissionDenied()
    if request.method == 'GET':
        form = ProblemForm()
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            problem.description = request.POST['description']
            problem.input= request.POST['input_description']
            problem.output = request.POST['output_description']
            problem.sample_in = request.POST['sample_in']
            problem.sample_out = request.POST['sample_out']
            problem.save()
            logger.info('post new problem, pid = %d' % (problem.pk))
            return redirect('/problem/%d' % (problem.pk))
    if not request.user.is_admin:
        del form.fields['owner']
    return render(request, 'problem/edit.html', 
                    { 'form': form, 'owner': request.user, 'is_new': True })

def preview(request):
    return render(request, 'problem/preview.html')

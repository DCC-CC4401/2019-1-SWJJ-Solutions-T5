# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import *
from evaluation.models import *

from .forms import *

from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def rubrics_list(request):
    if request.POST:
        newl = "%n%"
        data = request.POST
        name = data['name']
        mi = data['dur_min']
        ma = data['dur_max']
        t = data['table']
        t = t.replace('\t', '')
        t = t.replace('\r', '')
        rows = t.split(newl)
        rub = [rows[0].split('%,%')]
        for row in rows[1:len(rows)]:
            r = row.split('%,%')
            print(r)
            if r[0] != '':
                rub.append(r)

        empty_column_indexs = []
        for i in range(1, len(rub[0])):
            if rub[0][i] == '':
                empty_column_indexs.append(i)
        for idx in empty_column_indexs[::-1]:
            for row in rub:
                row.pop(idx)

        rubric = Rubric.objects.all()
        create = True
        for r in rubric:
            if r.name == name:
                create = False
        if create:
            ru = Rubric.objects.create(name=name, duration_min=mi, duration_max=ma, state=False)
            ru.set_rubric(rub)
            ru.save()
        return redirect('rubrics:rubrics')
    rubrics = Rubric.objects.all()
    return render(request,'rubrics/rubrics_list.html', {'rubrics': rubrics})


def create_rubric(request):
    rubrics = Rubric.objects.all()
    names = []
    for r in rubrics:
        names.append(r.name)
    return render(request, 'rubrics/rubrics_create.html', {"names": names})


def delete_rubric(request):
    if request.method=='POST':
        name=request.POST['name_rubric']
        rubric=Rubric.objects.get(name=name)
        rubric.delete()
        return redirect('rubrics:rubrics')
    rubrics = Rubric.objects.all()
    return render(request, '/rubrics/rubrics_list.html', {'rubrics': rubrics})


def rubric_details(request, rubric_key):
    rubric = Rubric.objects.get(name=rubric_key)
    rub = rubric.get_rubric()
    return render(request, 'rubrics/rubrics_details.html', {'rubric': rubric, 'levels': rub[0], 'rows': rub[1:]})


def rubric_modify(request, rubric_key):
    rubric = Rubric.objects.get(name=rubric_key)
    evaluation=Evaluation.objects.filter(rubric=rubric)
    for e in evaluation:
        grades=Evaluation_Student.objects.filter(evaluation_id=e)
        for g in grades:
            if (g.grade >0):
                messages.error(request, 'Esta rúbrica esta siendo utilizada en una evaluación. No puedes moficarla')
                rubrics=Rubric.objects.all()
                return redirect('rubrics:rubrics')
            
    rub = rubric.get_rubric()
    rubrics = Rubric.objects.all()
    names = []
    for r in rubrics:
        names.append(r.name)
    return render(request, 'rubrics/rubrics_modify.html', {'rubric': rubric, 'levels': rub[0], 'rows': rub[1:], 'names': names})


def rubric_modify_database(request, rubric_key):
    rubric = Rubric.objects.get(name=rubric_key)
    evaluations = Evaluation.objects.filter(rubric=rubric)
    ids_eval = []
    for eval in evaluations:
        ids_eval.append(eval.id)
    rubric.delete()
    newl = "%n%"
    if request.method == 'POST':
        data = request.POST
        name = data['name']
        mi = data['dur_min']
        ma = data['dur_max']
        t = data['table']
        t = t.replace('\t', '')
        t = t.replace('\r', '')
        rows = t.split(newl)
        rub = [rows[0].split('%,%')]
        for row in rows[1:len(rows)]:
            r = row.split('%,%')
            if r[0] != '':
                rub.append(r)
        empty_column_indexs = []
        for i in range(1, len(rub[0])):
            if rub[0][i] == '':
                empty_column_indexs.append(i)
        for idx in empty_column_indexs[::-1]:
            for row in rub:
                row.pop(idx)

        create = True
        rubric = Rubric.objects.all()
        for r in rubric:
            if r.name == name:
                create = False
        if create:
            ru = Rubric.objects.create(name=name, duration_min=mi, duration_max=ma, state=False)
            ru.set_rubric(rub)
            ru.save()
            for id in ids_eval:
                evaluation = Evaluation.objects.get(id=id)
                evaluation.rubric = ru
                evaluation.save()
    rubrics = Rubric.objects.all()
    return render(request, 'rubrics/rubrics_list.html', {'rubrics': rubrics})

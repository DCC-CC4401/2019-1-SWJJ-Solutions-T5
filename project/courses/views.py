# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages

from .models import Course, Student, Team, Student_Team

from django.shortcuts import render,redirect

from .forms import CourseForm

def courses_list(request):
    if request.method=='POST':
        title = request.POST['title']
        code= request.POST['code']
        semester = request.POST['semester']
        section = request.POST['section']
        year = request.POST['year']
        if (title != '' and code != '' and semester != '' and section != '' and year != ''):
            try:
                course = Course.objects.get(code = code,
                                           semester = semester,
                                           section = section, year = year)
                messages.error(request, 'La combinación de código, sección, semestre, año ya existe')
            except Course.DoesNotExist:
                course = Course.objects.create(title = title, code = code,
                                               semester = semester,
                                               section = section, year = year)
                course.save()
        courses = Course.objects.all().order_by('semester')
        return redirect('/courses', {'courses': courses})

    # else, no había request method POST
    courses = Course.objects.all().order_by('semester')
    return render(request,'courses/courses_list.html', {'courses': courses})

def delete_course(request):
    if request.method=='POST':
        id=request.POST['id_course']
        course=Course.objects.get(id=id)
        course.delete()
    courses= Course.objects.all().order_by('semester')
    return render(request, 'courses/courses_list.html',{'courses':courses})

def courses_modify(request, course_key):
    course_keys= course_key.split("-")
    course= Course.objects.get(code=course_keys[0], section=course_keys[1], year=course_keys[2], semester=course_keys[3])

    if request.method=='POST':
        title = request.POST['title']
        code= request.POST['code']
        semester = request.POST['semester']
        section = request.POST['section']
        year= request.POST['year']
    
        course.title=title
        course.code=code
        course.semester=semester
        course.section=section
        course.year=year
        course.save()


        return redirect('/courses')

    """Para cuando se seleccione el botón de curso"""

    # filter puede retornar más de un parámetro
    return render(request, 'courses/courses_modify.html', {'course': course})


def course_details(request, course_key):
    """Para cuando se seleccione el botón de curso"""
    course_keys= course_key.split("-")
    course= Course.objects.get(code=course_keys[0], section=course_keys[1], year=course_keys[2], semester=course_keys[3])
    teamsList= Team.objects.filter(course=course)

    data = []
    for team in teamsList:
        students= Student.objects.filter(team=team)
        data.append((team, students))
     # filter puede retornar más de un parámetro
    lenTeams= teamsList.count()
    print(lenTeams)
    return render(request, 'courses/course_details.html', {'course': course, 'teams': data, 'lenTeams': lenTeams})

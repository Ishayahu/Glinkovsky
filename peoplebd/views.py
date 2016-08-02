# -*- coding:utf-8 -*-
# coding=<utf8>
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from peoplebd.models import Person, Category, Days

admins = ('ishayahu','admin')

@login_required
def index(request):
    if request.user.get_username() in admins:
        filter = ''
        if request.method == 'POST':
            if 'necessarily' in request.POST:

                request.session["necessarily"] = request.POST['necessarily']
                if "busy" in request.session:
                    if request.session["busy"]:
                        peoples = Person.objects.filter(busy=True).filter(
                            category = request.POST['necessarily'])
                        filter = "+" + Category.objects.get(
                            id = request.POST['necessarily']).name + "; Занятые"
                    else:
                        peoples = Person.objects.filter(busy=False).filter(
                            category = request.POST['necessarily'])
                        filter = "+" + Category.objects.get(
                            id = request.POST['necessarily']).name + "; Свободные"
                else:
                    peoples = Person.objects.filter(category = request.POST['necessarily'])
                    filter = "+" + Category.objects.get(id=request.POST['necessarily']).name
            elif 'unnecessarily' in request.POST:
                request.session["unnecessarily"] = request.POST[
                    'unnecessarily']
                if "busy" in request.session:
                    if request.session["busy"]:
                        peoples = Person.objects.filter(busy=True).exclude(
                            category = request.POST['unnecessarily'])
                        filter = "-" + Category.objects.get(
                            id = request.POST['unnecessarily']).name + "; Занятые"
                    else:
                        peoples = Person.objects.filter(busy=False).exclude(
                            category = request.POST['unnecessarily'])
                        filter = "-" + Category.objects.get(
                            id = request.POST['unnecessarily']).name + "; Свободные"
                else:
                    peoples = Person.objects.exclude(category = request.POST['unnecessarily'])
                    filter = "-" + Category.objects.get(id=request.POST['unnecessarily']).name
                # peoples = Person.objects.filter(busy = False).exclude(category = request.POST['unnecessarily'])
                # filter = "-" + Category.objects.get(id=request.POST['unnecessarily']).name
            elif "busy" in request.POST:
                request.session['busy'] = True
                if "necessarily" in request.session:
                    peoples = Person.objects.filter(
                        busy = True).filter(
                        category = request.session['necessarily'])
                    filter = "+" + Category.objects.get(
                        id = request.session[
                            'necessarily']).name + "; Занятые"
                elif "unnecessarily" in request.session:
                    peoples = Person.objects.filter(
                        busy = True).exclude(
                        category = request.session['unnecessarily'])
                    filter = "-" + Category.objects.get(
                        id = request.session[
                            'unnecessarily']).name + "; Занятые"
                else:

                    peoples = Person.objects.filter(busy = True)
                    filter = "Занятые"
            else: # отмечено свободные
                request.session['busy'] = False
                if "necessarily" in request.session:
                    peoples = Person.objects.filter(
                        busy = False).filter(
                        category = request.session['necessarily'])
                    filter = "+" + Category.objects.get(
                        id = request.session[
                            'necessarily']).name + "; Свободные"
                elif "unnecessarily" in request.session:
                    peoples = Person.objects.filter(
                        busy = False).exclude(
                        category = request.session['unnecessarily'])
                    filter = "-" + Category.objects.get(
                        id = request.session[
                            'unnecessarily']).name + "; Свободные"
                else:
                    peoples = Person.objects.filter(busy = False)
                    filter = "Свободные"

        else:
            if "busy" in request.session:
                del request.session['busy']
            if "necessarily" in request.session:
                del request.session['necessarily']
            if "unnecessarily" in request.session:
                del request.session['unnecessarily']
            peoples = Person.objects.all()
        template = loader.get_template('peoplebd/all_list.html')
        categories = Category.objects.all()
        context = {
            'peoples': peoples,
            'categories': categories,
            'filter': filter,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("/peoplebd/user/")

@login_required
def profile(request, id=None, year=None, month=None):

    # получаем год и месяц для календаря и ссылок на прошлый/след месяц
    import datetime
    from dateutil.relativedelta import relativedelta
    if year is None:
        year = datetime.date.today().year
        month = datetime.date.today().month
    else:
        year = int(year)
        month = int(month)
    prev_month = dict()
    next_month = dict()
    import calendar
    import locale
    # locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    locale.setlocale(locale.LC_ALL, '')
    # mrange = calendar.monthrange(year, month)
    cal = calendar.monthcalendar(year,month)
    prev_month['year'] = (datetime.date(year,month,1)- relativedelta(months=1)).year
    prev_month['month'] = (datetime.date(year,month,1) - relativedelta(months=1)).month
    prev_month['name'] = calendar.month_name[prev_month['month']] + " " + str(prev_month['year'])
    next_month['year'] = (datetime.date(year,month,1) + relativedelta(months=1)).year
    next_month['month'] = (datetime.date(year,month,1) + relativedelta(months=1)).month
    next_month['name'] = calendar.month_name[next_month['month']] + " " + str(next_month['year'])

    login = request.user.get_username()
    from peoplebd.forms import ChangeProfile
    if id is None:
        try:
            user = Person.objects.get(login = login)
        except Person.DoesNotExist:
            # зареген, но без профиля - создаём профиль
            return HttpResponseRedirect("/peoplebd/create_profile/")
    else:
        # смотрим чужую страницу
        # проверяем, если открывается по id, то админ ли открывает
        if login not in admins:
            return HttpResponseRedirect("/peoplebd/user/")
        user = Person.objects.get(id=id)


    categories = Category.objects.all()
    template = loader.get_template('peoplebd/profile.html')
    # создаём форму на основе профиля и полученных данных, если есть

    context = {
        'user': user,
        'categories': categories,
        'calendar': make_calendar(user,year,month),
        'prev': prev_month,
        'next': next_month,
        'year': year,
        'month': month,
    }
    # если получаем данные
    if request.method == 'POST':
        if "save_cal" in request.POST:
            # print("saving_cal")
            # сохраняем календарь
            year = int(request.POST["year"])
            month = int(request.POST["month"])
            busy_days = [day.id for day in user.busy_days.all()]
            for day in range(32):
                if "day"+str(day) in request.POST:
                    # print(day)
                    try:
                        busy_day = Days.objects.get(year = year,month = month,day = day)
                    except Days.DoesNotExist:
                        busy_day = Days(year=year, month=month, day=day)
                        busy_day.save()
                    user.busy_days.add(busy_day)

                else:
                    try:
                        busy_day = Days.objects.get(year = year,month = month,day = day)
                        if busy_day.id in busy_days:
                            user.busy_days.remove(busy_day)
                    except Days.DoesNotExist:
                        # раз дня нет, значит точно не занят
                        pass
            user.save()
            return HttpResponseRedirect("/peoplebd/user/"+str(id)+"/"+request.POST["year"]+"/"+request.POST["month"]+"/")
        else:
            # сохраняем профиль
            f = ChangeProfile(request.POST)
            context['form'] = f
            if f.is_valid():
                # верно - всё сохраняем
                user.fio = f.cleaned_data['fio']
                user.mail = f.cleaned_data['mail']
                user.tel = f.cleaned_data['tel']
                user.busy = f.cleaned_data['busy']
                user.category.clear()
                for cat in f.cleaned_data['category']:
                    user.category.add(cat)
                user.save()
                return HttpResponseRedirect("/peoplebd/profile/")
            else:
                # не верно - просим исправить
                return HttpResponse(template.render(context, request))
    else:
        f = ChangeProfile(instance = user)
        context['form'] = f
        # получаем профиль
        return HttpResponse(template.render(context, request))



@login_required
def create_profile(request):
    login = request.user.get_username()
    categories = Category.objects.all()
    from peoplebd.forms import NewPerson
    template = loader.get_template('peoplebd/create_profile.html')
    f = NewPerson(request.POST)
    context = {
        'login': login,
        'categories': categories,
        'form': f,
    }
    if request.method == "POST":
        if f.is_valid():
            user = f.save()
            user.login = login
            user.save()
            if user.comment == 'None':
                user.comment = ""
            return HttpResponseRedirect("/peoplebd/profile/")
        else:
            return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render(context, request))

def make_calendar(user,year,month):
    busy_days = [day.day for day in user.busy_days.filter(year=year).filter(month=month)]
    # from calendar import LocaleTextCalendar
    # calendar = LocaleTextCalendar(locale = 'ru_RU')
    import calendar
    import locale
    # locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
    locale.setlocale(locale.LC_ALL, '')
    # mrange = calendar.monthrange(year, month)
    cal = calendar.monthcalendar(year,month)
    res = "<table border='1'>"
    res += "<tr><th colspan='7'>"+calendar.month_name[month]+ " "+ str(year)+"</th></tr>"
    weekdaynames = calendar.weekheader(2).split(" ")
    res += "<tr>"
    for wdn in weekdaynames:
        res += "<th>"+wdn+"</th>"
    res += "</tr>"
    for week in cal:
        res += "<tr>"
        for day in week:
            if day == 0:
                res += "<td></td>"
            else:
                if day in busy_days:
                    res += "<td><input type='checkbox' checked name='day" + str(day) + "'>" + str(day) + "</td>"
                else:
                    res += "<td><input type='checkbox' name='day"+str(day)+"'>"+str(day)+"</td>"
        res += "</tr>"
    res += "</table>"
    return res

# -*- coding:utf-8 -*-
# coding=<utf8>
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from peoplebd.models import Person, Category, Day

admins = ('ishayahu','admin')

@login_required
def index(request):
    if request.user.get_username() in admins:
        filter = ''
        import datetime
        today = datetime.date.today()
        try:
            today_day = Day.objects.get(year=today.year,
                                        month=today.month,
                                        day=today.day)
        except Day.DoesNotExist:
            # значит, все в этот день точно свободны
            # но для простоты мы его создадим
            today_day = Day(year=today.year,
                            month=today.month,
                            day=today.day)
            today_day.save()

        if request.method == 'POST':


            # ищем по требованию
            if 'necessarily' in request.POST:
                request.session["necessarily"] = request.POST['necessarily']
                # если уже ставили фильтр по занятости
                if "busy" in request.session:
                    # ищем занятых
                    if request.session["busy"]:
                        peoples = Person.objects.filter(busy_days = today_day).\
                            filter(category = request.POST['necessarily'])
                        filter = "+" + Category.objects.get(
                            id = request.POST['necessarily']).name + u"; Занятые"
                    # ищем свободных
                    else:
                        peoples = Person.objects.exclude(busy_days = today_day).filter(
                            category = request.POST['necessarily'])
                        filter = "+" + Category.objects.get(
                            id = request.POST['necessarily']).name + u"; Свободные"
                # на занятость побоку, фильтр не стоит
                else:
                    peoples = Person.objects.filter(category = request.POST['necessarily'])
                    busy_peoples_id = [p.id for p in Person.objects.filter(category = request.POST['necessarily']).filter(busy_days=today_day)]
                    for people in peoples:
                        if people.id in busy_peoples_id:
                            people.busy = True
                    filter = "+" + Category.objects.get(id=request.POST['necessarily']).name
            # аналогично
            elif 'unnecessarily' in request.POST:
                request.session["unnecessarily"] = request.POST[
                    'unnecessarily']
                if "busy" in request.session:
                    if request.session["busy"]:
                        peoples = Person.objects.filter(busy_days = today_day).exclude(
                            category = request.POST['unnecessarily'])
                        filter = "-" + Category.objects.get(
                            id = request.POST['unnecessarily']).name + u"; Занятые"
                    else:
                        peoples = Person.objects.exclude(busy_days = today_day).exclude(
                            category = request.POST['unnecessarily'])
                        filter = "-" + Category.objects.get(
                            id = request.POST['unnecessarily']).name + u"; Свободные"
                else:
                    peoples = Person.objects.exclude(category = request.POST['unnecessarily'])
                    busy_peoples_id = [p.id for p in Person.objects.exclude(category = request.POST['unnecessarily']).filter(busy_days=today_day)]
                    for people in peoples:
                        if people.id in busy_peoples_id:
                            people.busy = True

                    filter = "-" + Category.objects.get(id=request.POST['unnecessarily']).name
                # peoples = Person.objects.filter(busy = False).exclude(category = request.POST['unnecessarily'])
                # filter = "-" + Category.objects.get(id=request.POST['unnecessarily']).name
            # если учитываем занятость
            elif "busy" in request.POST:
                # ищем занятых
                request.session['busy'] = True
                if "necessarily" in request.session:
                    peoples = Person.objects.filter(
                        busy_days=today_day).filter(
                        category = request.session['necessarily'])
                    filter = "+" + Category.objects.get(
                        id = request.session[
                            'necessarily']).name + u"; Занятые"
                elif "unnecessarily" in request.session:
                    peoples = Person.objects.filter(
                        busy_days=today_day).exclude(
                        category = request.session['unnecessarily'])
                    filter = "-" + Category.objects.get(
                        id = request.session[
                            'unnecessarily']).name + u"; Занятые"
                else:
                    # всех занятых
                    peoples = Person.objects.filter(busy_days = today_day)
                    filter = "Занятые"
            else:
                # отмечено свободные
                request.session['busy'] = False
                if "necessarily" in request.session:
                    peoples = Person.objects.exclude(
                        busy_days=today_day).filter(
                        category = request.session['necessarily'])
                    filter = "+" + Category.objects.get(
                        id = request.session[
                            'necessarily']).name + u"; Свободные"
                elif "unnecessarily" in request.session:
                    peoples = Person.objects.exclude(
                        busy_days=today_day).exclude(
                        category = request.session['unnecessarily'])
                    filter = "-" + Category.objects.get(
                        id = request.session[
                            'unnecessarily']).name + u"; Свободные"
                else:
                    peoples = Person.objects.exclude(busy_days = today_day)
                    filter = "Свободные"

        else:
            if "busy" in request.session:
                del request.session['busy']
            if "necessarily" in request.session:
                del request.session['necessarily']
            if "unnecessarily" in request.session:
                del request.session['unnecessarily']
            # вообще всех
            peoples = Person.objects.all()
            busy_peoples_id = [p.id for p in Person.objects.filter(
                busy_days=today_day)]
            for people in peoples:
                if people.id in busy_peoples_id:
                    people.busy = True

        template = loader.get_template('peoplebd/all_list.html')
        categories = Category.objects.all()
        context = {
            'peoples': peoples,
            'categories': categories,
            'filter': filter,
            'busy': 'busy' in request.session and request.session['busy'] == True,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("/peoplebd/user/")

@login_required
def profile(request, id=None, year=None, month=None):
    if id is None:
        id = 0
    id = int(id)
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
    prev_month['name'] = calendar.month_name[prev_month['month']].decode('cp1251') + u" " + unicode(prev_month['year'])
    next_month['year'] = (datetime.date(year,month,1) + relativedelta(months=1)).year
    next_month['month'] = (datetime.date(year,month,1) + relativedelta(months=1)).month
    next_month['name'] = calendar.month_name[next_month['month']].decode('cp1251') + u" " + unicode(next_month['year'])

    login = request.user.get_username()
    from peoplebd.forms import ChangeProfile
    # user - тот, чей профиль смотрим
    # visiter - тот, кто смотрит страницу
    try:
        visiter = Person.objects.get(login=login)
    except Person.DoesNotExist:
        # смотрящий зареген, но без профиля - создаём профиль
        return HttpResponseRedirect("/peoplebd/create_profile/")

    if id == 0 or id == visiter.id:
        # то есть, открываем страницу типа http://127.0.0.1:8000/peoplebd/user/ - хотим посмотреть свой профиль
        # или запрашиваем свой id
        user = visiter
    else:
        # смотрим чужую страницу
        # проверяем, если открывается по id, то админ ли открывает
        user = Person.objects.get(id=id)
        if login not in admins:
            return HttpResponseRedirect("/peoplebd/user/")


    categories = Category.objects.all()
    template = loader.get_template('peoplebd/profile.html')
    # создаём форму на основе профиля и полученных данных, если есть

    context = {
        'user': user,
        'categories': categories,
        # 'calendar': "<b>CAL</b>",
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
                        busy_day = Day.objects.get(year = year, month = month, day = day)
                    except Day.DoesNotExist:
                        busy_day = Day(year=year, month=month, day=day)
                        busy_day.save()
                    user.busy_days.add(busy_day)
                    user.save()

                else:
                    try:
                        busy_day = Day.objects.get(year = year, month = month, day = day)
                        if busy_day.id in busy_days:
                            user.busy_days.remove(busy_day)
                            user.save()
                    except Day.DoesNotExist:
                        # раз дня нет, значит точно не занят
                        pass
            # user.save()
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
                # user.busy = f.cleaned_data['busy']
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

@login_required
def delete_profile(request,id):
    if request.user.get_username() not in admins:
        return HttpResponseRedirect("/")
    from django.contrib.auth.models import User
    p = Person.objects.get(id=id)
    pp = User.objects.get(username=p.login)
    pp.delete()
    p.delete()
    return HttpResponseRedirect("/")


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
    res = u"<table border='1'>"
    res += u"<tr><th colspan='7'>"+calendar.month_name[month].decode('cp1251')+ u" "+ unicode(year)+u"</th></tr>"
    weekdaynames = calendar.weekheader(2).split(" ")
    res += u"<tr>"
    for wdn in weekdaynames:
        res += u"<th>"+wdn.decode('cp1251')+u"</th>"
    res += u"</tr>"
    for week in cal:
        res += u"<tr>"
        for day in week:
            if day == 0:
                res += u"<td></td>"
            else:
                if day in busy_days:
                    res += u"<td><input type='checkbox' checked name='day" + unicode(day) + u"'>" + unicode(day) + u"</td>"
                else:
                    res += u"<td><input type='checkbox' name='day"+unicode(day)+u"'>"+unicode(day)+u"</td>"
        res += u"</tr>"
    res += u"</table>"
    return res

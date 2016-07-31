from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from peoplebd.models import Person, Category

@login_required
def index(request):
    if request.user.get_username() in ('ishayahu','admin'):
        filter = ''
        if request.method == 'POST':
            if 'necessarily' in request.POST:
                peoples = Person.objects.filter(busy = False).filter(category = request.POST['necessarily'])
                filter = "+" + Category.objects.get(id=request.POST['necessarily']).name
            elif 'unnecessarily' in request.POST:
                peoples = Person.objects.filter(busy = False).exclude(category = request.POST['unnecessarily'])
                filter = "-" + Category.objects.get(id=request.POST['unnecessarily']).name
        else:
            peoples = Person.objects.filter(busy = False)
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
def profile(request):
    login = request.user.get_username()
    try:
        user = Person.objects.get(login = login)
    except Person.DoesNotExist:
        # зареген, но без профиля
        return HttpResponseRedirect("/peoplebd/create_profile/")
    if request.method == 'POST':
        raise NotImplementedError()
    else:
        categories = Category.objects.all()
        template = loader.get_template('peoplebd/profile.html')
        context = {
            'user': user,
            'categories': categories,
        }
        return HttpResponse(template.render(context, request))

@login_required
def create_profile(request):
    login = request.user.get_username()
    categories = Category.objects.all()
    template = loader.get_template('peoplebd/create_profile.html')
    context = {
        'login': login,
        'categories': categories,
    }
    if request.method == "POST":
        raise NotImplementedError()

        user = Person(fio = request.POST['fio'],
                      tel = request.POST['tel'],
                      login = request.POST['login'])
        user.save()
        for cat in request.POST['category']:
            user.category.add(Category.objects.get(id=cat))
        user.save()
        return HttpResponseRedirect("/peoplebd/profile/")

    else:
        return HttpResponse(template.render(context, request))


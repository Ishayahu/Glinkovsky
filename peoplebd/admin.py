# -*- coding:utf-8 -*-
# coding=<utf8>
from django.contrib import admin
from peoplebd.models import Person, Category, Day

# Register your models here.
admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Day)

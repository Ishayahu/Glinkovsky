# -*- coding:utf-8 -*-
# coding=<utf8>
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets

from peoplebd.models import Person, Category
class NewPerson(ModelForm):
    class Meta:
        model = Person
        fields = ['fio','tel','category','busy']
        labels = {
            'fio': 'ФИО',
            'tel': 'Телефон (10 знаков)',
            'mail': 'Почта',
            'category': 'Виды работ  (выбор при помощи ctrl)',
            'busy': 'Отметьте, если сейчас заняты'
        }
        # fields = '__all__' # for 1.8
        localized_fields = '__all__'


class ChangeProfile(ModelForm):
    class Meta:
        model = Person
        fields = ['fio', 'tel', 'mail', 'category', 'busy']
        labels = {
            'fio': 'ФИО',
            'tel': 'Телефон (10 знаков)',
            'mail': 'Почта',
            'category': 'Виды работ (выбор при помощи ctrl)',
            'busy': 'Отметьте, если сейчас заняты'
        }
        # fields = '__all__' # for 1.8
        localized_fields = '__all__'

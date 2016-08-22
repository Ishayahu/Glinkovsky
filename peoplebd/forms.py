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
        fields = ['fio','tel','category']
        labels = {
            'fio': 'ФИО',
            'tel': 'Телефон (10 знаков. Например 9015553322)',
            'category': 'Виды работ  (выбор при помощи ctrl)',
        }
        localized_fields = '__all__'


class ChangeProfile(ModelForm):
    mail = forms.EmailField(required=True, label="Почта")
    class Meta:
        model = Person
        fields = ['fio', 'tel', 'mail', 'category']
        labels = {
            'fio': 'ФИО',
            'tel': 'Телефон (10 знаков. Например 9015553322)',
            'category': 'Виды работ (выбор при помощи ctrl)',
        }
        localized_fields = '__all__'

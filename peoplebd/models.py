# -*- coding:utf-8 -*-
# coding=<utf8>
from django.db import models
from django.core.validators import RegexValidator

class Person(models.Model):
    fio = models.CharField(max_length=200)
    # tel = models.CharField(max_length=10)
    phone_regex = RegexValidator(regex = r'^\d{10}$',
                                 message = "Phone number must be entered in the format: '9051112233'. Only 10 digits allowed.")
    tel = models.CharField(validators = [phone_regex], max_length=10)  # validators should be a list
    mail = models.EmailField(blank = True, null = True)
    # rating = models.CharField(max_length=30, blank = True,
    #                            null = True)
    RATING_CHOICES = (
        (0, u'Руки из жопы'),
        (1, u'Нет отпыта'),
        (2, u'Норма'),
        (3, u'Хорош'),
        (4, u'Мастер от Б-га'),
    )
    rating = models.IntegerField(
        choices = RATING_CHOICES,
        default = 2,
    )
    login = models.CharField(max_length=140, blank = True,
                             null = True)
    # busy = models.BooleanField()
    category = models.ManyToManyField('Category',
                                    related_name = "who_do",
                                    blank = True)
    busy_days = models.ManyToManyField('Days',related_name="who_busy", blank=True)
    comment = models.TextField(blank = True, null = True)

    def rating_verbose (self):
        return dict(Person.RATING_CHOICES).get(self.rating,'')

    def __unicode__(self):
        return self.fio+u";"+self.login
        # return u";".join((self.fio.decode('utf-8'),self.login.decode('utf-8')))

    # def __str__(self):
    #     return ";".join((self.fio,str(self.login),str(self.busy)))

    class Meta:
        ordering = ['fio',]

class Days(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    def __str__(self):
        return "/".join((str(self.day),str(self.month), str(self.year)))

    def __unicode__(self):
        return u"/".join((str(self.day),str(self.month), str(self.year)))


class Category(models.Model):
    name = models.CharField(max_length = 500)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"{}".format(self.name)

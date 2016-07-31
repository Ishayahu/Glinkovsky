from django.db import models


class Person(models.Model):
    fio = models.CharField(max_length=200)
    tel = models.CharField(max_length=10)
    mail = models.EmailField(blank = True, null = True)
    rating = models.CharField(max_length=30, blank = True,
                               null = True)
    login = models.CharField(max_length=140, blank = True,
                             null = True)
    busy = models.BooleanField()
    category = models.ManyToManyField('Category',
                                    related_name = "who_do",
                                    blank = True)
    comment = models.TextField(blank = True, null = True)

    def __unicode__(self):
        return u";".join((self.fio,str(self.login)))

    def __str__(self):
        return ";".join((self.fio,str(self.login),str(self.busy)))

    class Meta:
        ordering = ['fio',]

class Category(models.Model):
    name = models.CharField(max_length = 500)

    def __str__(self):
        return self.name

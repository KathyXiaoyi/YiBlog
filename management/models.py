# coding:utf-8
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=256)
    create_date = models.DateTimeField(editable=True)

    def __unicode__(self):
        return self.role_name


class User(models.Model):
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=50)
    role = models.ForeignKey(Role)
    create_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __unicode__(self):
        self.username




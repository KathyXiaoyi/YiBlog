# coding:utf-8
from django.db import models
from management.models import User


class Group(models.Model):
    group_name = models.CharField(max_length=256)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.group_name


class Blog(models.Model):
    name = models.CharField(max_length=256)
    keywords = models.CharField(max_length=256)
    upload_date = models.DateTimeField(auto_now_add=True, editable=True)
    content = models.TextField()
    image = models.ImageField(upload_to='./img')
    group = models.ForeignKey(Group)
    # writer = models.ForeignKey(User)
    recommend_level = models.IntegerField()
    type = models.IntegerField()  # 1-原创； 2-转载

    def __unicode__(self):
        return self.name

# class Blog(models.Model):
#     name = models.CharField(max_length=256)
#     keywords = models.CharField(max_length=256)
#     upload_date = models.DateTimeField(auto_now_add=True, editable=True)
#     content = models.TextField()
#     image = models.CharField(max_length=256)
#     group = models.ForeignKey(Group)
#     # writer = models.ForeignKey(User)
#     recommend_level = models.IntegerField()
#     type = models.IntegerField()    # 1-原创； 2-转载
#
#     def __unicode__(self):
#         return self.name




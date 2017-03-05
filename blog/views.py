# coding:utf-8
from django.shortcuts import render
from blog.models import Group, Blog


def blog_detail(request):
    id = request.GET['id']
    b = Blog.objects.get(id=id)
    blog_last = Blog.objects.filter(id__lt=id).order_by('id')
    blog_next = Blog.objects.filter(id__gt=id)
    if blog_last:
        blog_last = blog_last.reverse()[0]
    if blog_next:
        blog_next = blog_next[0]
    group = b.group
    blog_list = Blog.objects.filter(group=group)
    # 获取所有的博客分组列表
    group_list = Group.objects.all()
    # 获取所有的博客列表
    new_blog_list = Blog.objects.order_by('-upload_date')[0:5]
    # 获取推荐文章（前5篇）
    rec_blog_list = Blog.objects.order_by('-recommend_level')[0:5]
    return render(request, 'blog/detail.html', {'blog': b, 'blog_last': blog_last, 'blog_next': blog_next,
                                                'blog_list': blog_list, 'group_list': group_list,
                                                'new_blog_list': new_blog_list, 'rec_blog_list': rec_blog_list})


def index(request):
    # 获取所有的博客分组列表
    group_list = Group.objects.all()
    # 获取所有的博客列表
    new_blog_list = Blog.objects.order_by('-upload_date')[0:5]
    # 获取推荐文章（前5篇）
    rec_blog_list = Blog.objects.order_by('-recommend_level')[0:5]
    return render(request, 'blog/index.html', {'group_list': group_list,
                                               'new_blog_list': new_blog_list, 'rec_blog_list': rec_blog_list})


def blog(request):
    try:
        id = request.GET['id']
        # 获取所有博客
        group = Group.objects.get(id=id)
        blog_list = Blog.objects.filter(group=group)
        # 获取所有博客
    except KeyError:
        try:
            keyword = request.GET['keyword']
            blog_list = Blog.objects.filter(name__contains=keyword)
        except KeyError:
            blog_list = Blog.objects.all()
    # 获取所有的博客分组列表
    group_list = Group.objects.all()
    # 获取所有的博客列表
    new_blog_list = Blog.objects.order_by('-upload_date')[0:5]
    # 获取推荐文章（前5篇）
    rec_blog_list = Blog.objects.order_by('recommend_level')[0:5]
    return render(request, 'blog/blog.html', {'group_list': group_list, 'new_blog_list': new_blog_list,
                                              'rec_blog_list': rec_blog_list, 'blog_list': blog_list})


def about(request):
    # 获取所有的博客分组列表
    group_list = Group.objects.all()
    # 获取所有的博客列表
    new_blog_list = Blog.objects.order_by('-upload_date')[0:5]
    # 获取推荐文章（前5篇）
    rec_blog_list = Blog.objects.order_by('recommend_level')[0:5]
    return render(request, 'blog/about.html', {'group_list': group_list,
                                               'new_blog_list': new_blog_list, 'rec_blog_list': rec_blog_list})




# coding:utf-8
from django.shortcuts import render, HttpResponse, render_to_response, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from management.models import Role, User
from blog.models import Group, Blog

import json
import datetime


@csrf_exempt
def logout(request):
    if request.is_ajax() and request.method == 'POST':
        request.session.flush()
        result = {'status': '1', 'info': '已成功退出！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        result = {'status': '1', 'info': '已成功退出！'}
        return HttpResponse(json.dumps(result), content_type='application/json')


def admin_login(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username is None:
                result = {'status': '0', 'info': '用户名不能为空！'}
                return HttpResponse(json.dumps(result), content_type='application/json')
            elif password is None:
                result = {'status': '0', 'info': '密码不能为空！'}
                return HttpResponse(json.dumps(result), content_type='application/json')
            u = User.objects.get(username=username)
            if u.password == password:
                if request.session is None:
                    request.session['username'] = username
                else:
                    name = request.session.get('username', False)
                    if name is False:
                        request.session['username'] = username
                result = {'status': '1', 'info': '验证成功！', "userId": str(u.id)}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {'status': '0', 'info': '密码错误！'}
                return HttpResponse(json.dumps(result), content_type='application/json')
        except ObjectDoesNotExist:
            result = {'status': '0', 'info': '用户名不存在！'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        except Exception, e:
            result = {'status': '0', 'info': '出现错误！%s' % e}
            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render(request, 'public/login.html')


def login(request):
    if request.is_ajax() and request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None:
            result = {'status': '0', 'info': '用户名不能为空！'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        elif password is None:
            result = {'status': '0', 'info': '密码不能为空！'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        try:
            u = User.objects.get(username=username)
            if u.password == password:
                if request.session is None:
                    request.session['username'] = username
                else:
                    name = request.session.get('username', False)
                    if name is False:
                        request.session['username'] = username
                result = {'status': '1', 'info': '验证成功！', "userId": str(u.id)}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {'status': '0', 'info': '密码错误！'}
                return HttpResponse(json.dumps(result), content_type='application/json')
        except ObjectDoesNotExist:
            result = {'status': '0', 'info': '用户名不存在！'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        except Exception, e:
            result = {'status': '0', 'info': '出现错误！%s' %e}
            return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'blog/index.html')


def admin_index(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    else:
        user_id = request.GET['id']
        u = User.objects.get(id=user_id)
        return render(request, 'public/index.html', {'user': u})


# 角色管理Index
def role(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    # 从数据库中读取全部的角色信息
    role_list = Role.objects.all()
    return render_to_response('role/index.html', {'role_list': role_list})


# 新增角色
def add_role(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        role_name = request.POST.get('role_name')
        if role_name is None:
            result = {'status': '0', 'info': '角色名不能为空！'}
        else:
            try:
                Role.objects.get(role_name=role_name)
            except ObjectDoesNotExist:
                r = Role(role_name=role_name)
                r.create_date = datetime.datetime.now()
                r.save()
            result = {'status': '1', 'info': '新角色创建成功！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'role/add.html')


# 修改角色信息
def edit_role(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        try:
            role_id = request.POST.get('role_id')
            new_name = request.POST.get('new_name')
            r = Role.objects.get(id=role_id)
            r.role_name = new_name
            r.save()
            result = {'status': '1', 'info': '角色信息修改成功！'}
        except ObjectDoesNotExist:
            result = {'status': '0', 'info': '角色信息修改过程出现错误！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        try:
            role_id = request.GET['id']
            r = Role.objects.get(id=role_id)
        except ObjectDoesNotExist:
            r = None
        return render(request, 'role/edit.html', {'role': r})


# 用户管理Index
def user(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    # 从数据库中读取全部的用户信息
    user_list = User.objects.all()
    return render_to_response('user/index.html', {'user_list': user_list})


# 新增用户
def add_user(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 外键引用role 的直接赋值是否正确！！！
        user_role = request.POST.get('role')
        if user_name is None:
            result = {'status': '0', 'info': '用户名不能为空！'}
        elif password is None:
            result = {'status': '0', 'info': '密码不能为空！'}
        elif user_role is None:
            result = {'status': '0', 'info': '请指定用户角色！'}
        else:
            try:
                User.objects.get(username=user_name)
                result = {'status': '0', 'info': '该用户名已被占用，请更换用户名后重试！'}
            except ObjectDoesNotExist:
                u = User(username=user_name)
                u.password = password
                u.email = email
                u.role = Role.objects.get(id=user_role)
                u.save()
                result = {'status': '1', 'info': '新用户创建成功！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        role_list = Role.objects.all()
        return render(request, 'user/add.html', {'role_list': role_list})


# 编辑用户信息
def edit_user(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            new_password = request.POST.get('new_psw')
            new_email = request.POST.get('new_emil')
            new_role = request.POST.get('new_role')
            u = User.objects.get(id=user_id)
            u.password = new_password
            u.email = new_email
            u.role = Role.objects.get(id=new_role)
            u.save()
            result = {'status': '1', 'info': '用户信息修改成功！'}
        except ObjectDoesNotExist:
            result = {'status': '0', 'info': '用户信息修改过程出现错误！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        try:
            user_id = request.GET['id']
            u = User.objects.get(id=user_id)
            role_list = Role.objects.all()
        except ObjectDoesNotExist:
            u = None
        return render(request, 'user/edit.html', {'user': u, 'role_list': role_list})


def blog(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    blog_list = Blog.objects.all()
    return render(request, 'blogs/index.html', {'blog_list': blog_list})


def add_blog(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        try:
            blog_name = request.POST['blog_name']
            blog_keyword = request.POST['blog_keyword']
            blog_content = request.POST['blog_content']
            type_id = request.POST['type_id']
            group_id = request.POST['group_id']
            rec_index = request.POST['rec_index']
            img_url = request.POST['img_url']
            if blog_name is None:
                result = {'status': '0', 'info': '博客名称不能为空!'}
            elif blog_keyword is None:
                result = {'status': '0', 'info': '博客关键字不能为空!'}
            elif blog_content is None:
                result = {'status': '0', 'info': '博客内容不能为空!'}
            else:
                try:
                     Blog.objects.get(name=blog_name)
                except ObjectDoesNotExist:
                    g = Group.objects.get(id=group_id)
                    b = Blog(name=blog_name, keywords=blog_keyword, content=blog_content,
                              image=img_url, group=g, recommend_level=rec_index, type=type_id)
                    b.save()
                    result = {'status': '1', 'info': '新博客创建成功！'}
        except Exception, e:
            result = {'status': '0', 'info': '出现错误：%s' %e}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        # 获取所有的博客分组数据
        group_list = Group.objects.all()
        return render_to_response('blogs/add.html', {'group_list': group_list})


def edit_blog(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        try:
            blog_id = request.POST['blog_id']
            blog_keyword = request.POST['blog_keyword']
            blog_content = request.POST['blog_content']
            type_id = request.POST['type_id']
            group_id = request.POST['group_id']
            rec_index = request.POST['rec_index']
            b = Blog.objects.get(id=blog_id)
            b.keywords = blog_keyword
            b.content = blog_content
            g = Group.objects.get(id=group_id)
            b.group = g
            b.recommend_level = rec_index
            b.type = type_id
            b.save()
            result = {'status': '1', 'info': '博客信息修改成功！'}
        except ObjectDoesNotExist:
            result = {'status': '0', 'info': '博客修改过程出现错误！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        try:
            blog_id = request.GET['id']
            b = Blog.objects.get(id=blog_id)
            group_list = Group.objects.all()
        except ObjectDoesNotExist:
            b = None
            group_list = None
        return render(request, 'blogs/edit.html', {'blog': b, 'group_list': group_list})


# 管理所有的分组Index
def group(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    # 从数据库中读取全部的博客分组信息
    group_list = Group.objects.all()
    return render_to_response('group/index.html', {'group_list': group_list})


# 新增博客分组
def add_group(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name is None:
            result = {'status': '0', 'info': '分组名称不能为空'}
        else:
            try:
                Group.objects.get(group_name=group_name)
            except ObjectDoesNotExist:
                r = Group(group_name=group_name)
                r.save()
            result = {'status': '1', 'info': '新分组创建成功！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'group/add.html')


# 修改分组信息
def edit_group(request):
    username = request.session.get('username', False)
    if username is False:
        return HttpResponseRedirect('login')
    if request.is_ajax() and request.method == 'POST':
        try:
            group_id = request.POST.get('group_id')
            new_name = request.POST.get('new_name')
            g = Group.objects.get(id=group_id)
            g.group_name = new_name
            g.save()
            result = {'status': '1', 'info': '分组信息修改成功！'}
        except ObjectDoesNotExist:
            result = {'status': '0', 'info': '分组信息修改过程出现错误！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        try:
            group_id = request.GET['id']
            g = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            g = None
        return render(request, 'group/edit.html', {'group': g})


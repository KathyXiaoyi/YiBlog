# coding:utf-8
from django.shortcuts import render, HttpResponse, render_to_response, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from management.models import Role, User
from blog.models import Group, Blog
import json,  time, datetime, os
from PIL import Image


# 删除某个角色，并将该角色下的所有用户移至‘普通用户’
def delete_role(request):
    if request.is_ajax() and request.method == 'POST':
        role_id = request.POST.get('role_id')
        if role_id is None:
            result = {'status': '0', 'info': '出现错误：待删除的角色ID不能为空！'}
        else:
            role = Role.objects.get(id=role_id)
            if role.role_name == 'Default':
                result = {'status': '0', 'info': '角色Default为默认角色，不可删除！'}
            else:
                try:
                    # 删除角色之前，将该角色下的所有用户修改到"Default"角色下
                    user_list = User.objects.filter(role=role_id)
                    default_role = Role.objects.get(role_name='Default')
                    for user in user_list:
                        user.role = default_role
                        user.save()
                    Role.objects.get(id=role_id).delete()
                    result = {'status': '1', 'info': '已成功删除该角色！'}
                except ObjectDoesNotExist:
                    result = {'status': '1', 'info': '待删除的角色不存在！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'role/index.html')


# 删除某个博客
def delete_blog(request):
    if request.is_ajax() and request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        if blog_id is None:
            result = {'status': '0', 'info': '出现错误：待删除的博客ID不能为空！'}
        else:
            try:
                b = Blog.objects.get(id=blog_id)
                # 删除该博客对应的图片
                import sae.storage
                from sae.storage import Bucket
                bucket = Bucket('img')
                img_file = b.image.url
                file_name = img_file[-14:]
                if file_name != 'default000.jpg':
                    bucket.delete_object(file_name)
                b.delete()
                result = {'status': '1', 'info': '已成功删除该博客！'}
            except ObjectDoesNotExist:
                result = {'status': '1', 'info': '待删除的博客不存在！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'blogs/index.html')


# 删除某个分组，并将该分组下的所有博客移至Default分组下
def delete_group(request):
    if request.is_ajax() and request.method == 'POST':
        group_id = request.POST.get('group_id')
        if group_id is None:
            result = {'status': '0', 'info': '出现错误：待删除的分组ID不能为空！'}
        else:
            try:
                group = Group.objects.get(id=group_id)
                if group.group_name == 'Default':
                    result = {'status': '0', 'info': '分组Default为默认分组，不可删除！'}
                else:
                    # 删除分组之前，首先将该分组下的所有博客的分组修改为Default
                    blog_list = Blog.objects.filter(group=group_id)
                    default_group = Group.objects.get(group_name='Default')
                    for blog in blog_list:
                        blog.group = default_group
                        blog.save()
                    Group.objects.get(id=group_id).delete()
                    result = {'status': '1', 'info': '已成功删除该分组！'}
            except ObjectDoesNotExist:
                result = {'status': '1', 'info': '待删除的分组不存在！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'group/index.html')


# 删除某个用户
def delete_user(request):
    if request.is_ajax() and request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id is None:
            result = {'status': '0', 'info': '出现错误：待删除的用户ID不能为空！'}
        else:
            try:
                u = User.objects.get(id=user_id)
                if u.username != 'admin':
                    u.delete()
                    result = {'status': '1', 'info': '已成功删除该用户！'}
                else:
                    result = {'status': '0', 'info': 'admin为超级管理员，不可删除！'}
            except ObjectDoesNotExist:
                result = {'status': '1', 'info': '待删除的用户不存在！'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'user/index.html')


@csrf_exempt
def search_role(request):
    keywords = request.POST['keywords']
    if keywords is None:
        roles = None
    else:
        roles = Role.objects.all().filter(role_name__contains=keywords)
    return render(request, 'role/index.html', {'role_list': roles})


@csrf_exempt
def search_blog(request):
    keywords = request.POST['keywords']
    if keywords is None:
        blogs = None
    else:
        blogs = Blog.objects.all().filter(name__contains=keywords)
    return render(request, 'blogs/index.html', {'blog_list': blogs})


@csrf_exempt
def search_blog_keyword(request):
    keywords = request.POST['keywords']
    if keywords is None:
        blogs = None
    else:
        blogs = Blog.objects.all().filter(name__contains=keywords)
    blog_list = Blog.objects.all()
    # 获取所有的博客分组列表
    group_list = Group.objects.all()
    # 获取所有的博客列表
    new_blog_list = Blog.objects.order_by('-upload_date')[0:5]
    # 获取推荐文章（前5篇）
    rec_blog_list = Blog.objects.order_by('recommend_level')[0:5]
    return render(request, 'blog/blog.html', {'group_list': group_list, 'new_blog_list': new_blog_list,
                                              'rec_blog_list': rec_blog_list, 'blog_list': blog_list})


@csrf_exempt
def search_group(request):
    keywords = request.POST['keywords']
    if keywords is None:
        groups = None
    else:
        groups = Group.objects.all().filter(group_name__contains=keywords)
    return render(request, 'group/index.html', {'group_list': groups})


@csrf_exempt
def search_user(request):
    keywords = request.POST['keywords']
    if keywords is None:
        users = None
    else:
        users = User.objects.all().filter(username__contains=keywords)
    return render(request, 'user/index.html', {'user_list': users})


# # 本地开发使用
# @csrf_exempt
# def img_upload(request):
#     try:
#         reqfile = request.FILES['upload_file']
#         img = Image.open(reqfile)
#         if img is None:
#             result = {'status': '1', 'info': '图片为空！'}
#             return HttpResponse(json.dumps(result), content_type='application/json')
#         else:
#             # 对图片进行等比缩放
#             img.thumbnail((500, 500), Image.ANTIALIAS)
#             str_time = str(time.mktime(datetime.datetime.now().timetuple()))
#             str_time = str_time[:-2]
#             url = "static/var/image/" + str_time + ".png"
#             # 保存图片
#             img.save(url, "png")
#             result = {'status': '1', 'info': '图片上传成功！', 'url':url}
#             return HttpResponse(json.dumps(result), content_type='application/json')
#     except Exception, e:
#         result = {'status': '0', 'info': '图片上传出现错误：%s' %e}
#         return HttpResponse(json.dumps(result), content_type='application/json')

# import sae.storage
# s = sae.storage.Client()
# ob = sae.storage.Object(reqfile.read())
# url = s.put(domain_name, reqfile.name, ob)


# 部署时使用
@csrf_exempt
def img_upload(request):
    try:
        reqfile = request.FILES['upload_file']
        if reqfile is None:
            result = {'status': '1', 'info': '图片为空！'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            from os import environ
            online = environ.get("APP_NAME", "")
            if online:
                import sae.const
                access_key = sae.const.ACCESS_KEY
                secret_key = sae.const.SECRET_KEY
                appname = sae.const.APP_NAME
                domain_name = "img"  # 刚申请的domain
                str_time = str(time.mktime(datetime.datetime.now().timetuple()))
                str_time = str_time[:-2]
                reqfile.name = str_time + ".png"
                import sae.storage
                from sae.storage import Bucket
                bucket = Bucket('img')
                bucket.put()
                # http://www.sinacloud.com/doc/sae/python/storage.html
                bucket.put_object(reqfile.name, reqfile, content_type='application/x-www-form-urlencoded ')
                url = bucket.generate_url(reqfile.name)
                result = {'status': '1', 'info': '图片上传成功！', 'url':url}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result = {'status': '0', 'info': '图片上传出现错误！'}
                return HttpResponse(json.dumps(result), content_type='application/json')
    except Exception, e:
        result = {'status': '0', 'info': '图片上传出现错误：%s' %e}
        return HttpResponse(json.dumps(result), content_type='application/json')

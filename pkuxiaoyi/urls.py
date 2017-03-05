# coding:utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'blog.views.index', name='index'),
                       url(r'^blog$', 'blog.views.blog', name='blog'),
                       url(r'^about$', 'blog.views.about', name='about'),
                       url(r'^detail$','blog.views.blog_detail', name='detail'),
                       # url(r'^admin/test', 'blog.views.about', name='about'),

                       url(r'^login$', 'management.views.login', name='admin_login'),
                       url(r'^admin/index$', 'management.views.admin_index', name='admin_index'),
                       url(r'^admin/login$', 'management.views.admin_login', name='login'),
                       url(r'^admin/logout$', 'management.views.logout', name='logout'),


                       # 博客管理页面
                       url(r'^admin/blog$', 'management.views.blog', name='admin_blog'),
                       url(r'^admin/blog/add$', 'management.views.add_blog', name='admin_blog_add'),
                       url(r'^admin/blog/edit$', 'management.views.edit_blog', name='admin_blog_edit'),
                       url(r'^admin/blog/delete$', 'service.views.delete_blog', name='admin_blog_delete'),
                       url(r'^admin/blog/search$', 'service.views.search_blog', name='admin_blog_search'),
                       url(r'^admin/blog/keywords/search$', 'service.views.search_blog_keyword', name='blog_search'),


                       # 博客分组管理页面
                       url(r'^admin/group$', 'management.views.group', name='admin_group'),
                       url(r'^admin/group/add$', 'management.views.add_group', name='admin_group_add'),
                       url(r'^admin/group/edit$', 'management.views.edit_group', name='admin_group_edit'),
                       url(r'^admin/group/delete$', 'service.views.delete_group', name='admin_group_delete'),
                       url(r'^admin/group/search$', 'service.views.search_group', name='admin_group_search'),

                       # 用户管理页面
                       url(r'^admin/user$', 'management.views.user', name='admin_user'),
                       url(r'^admin/user/add$', 'management.views.add_user', name='admin_user_add'),
                       url(r'^admin/user/edit$', 'management.views.edit_user', name='admin_user_edit'),
                       url(r'^admin/user/delete$', 'service.views.delete_user', name='admin_user_delete'),
                       url(r'^admin/user/search$', 'service.views.search_user', name='admin_user_search'),

                       # 角色管理页面
                       url(r'^admin/role$', 'management.views.role', name='admin_role'),
                       url(r'^admin/role/add$', 'management.views.add_role', name='admin_role_add'),
                       url(r'^admin/role/edit$', 'management.views.edit_role', name='admin_role_edit'),
                       url(r'^admin/role/delete$', 'service.views.delete_role', name='admin_role_delete'),
                       url(r'^admin/role/search$', 'service.views.search_role', name='admin_role_search'),

                       url(r'^admin/img/upload', 'service.views.img_upload'),
)



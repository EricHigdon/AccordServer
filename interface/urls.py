from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^support/$', views.support, name='support'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^news/$', views.news, name='news'),
    url(r'^news/delete/(?P<item_pk>[0-9]+)/$', views.delete_item, name='delete_item'),
    url(r'^news/reorder/$', views.reorder_item, name='reorder_item'),
    url(r'^im-new/$', views.im_new, name='im_new'),
    url(r'^change-password/$', auth_views.password_change, {'post_change_redirect':'my_church', 'template_name':'interface/password-change.html'}, name='password_change'),
    url(r'^connect/$', views.connect, name='connect'),
    url(r'^connect/delete/(?P<form_pk>[0-9]+)/$', views.delete_form, name='delete_form'),
    url(r'^connect/reorder/$', views.reorder_form, name='reorder_form'),
    url(r'^service/$', views.service, name='service'),
    url(r'^service/delete/(?P<item_pk>[0-9]+)/$', views.delete_passage, name='delete_passage'),
    url(r'^service/reorder/$', views.reorder_passage, name='reorder_passage'),
    url(r'^send-message/$', views.send_message, name='send_message'),
    url(r'^my-church/$', views.my_church, name='my_church'),
    url(r'^home/$', views.home, name='home'),
    url(r'^display/$', views.display, name='display'),
    url(r'^display/delete/(?P<item_pk>[0-9]+)/$', views.delete_slide, name='delete_slide'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]

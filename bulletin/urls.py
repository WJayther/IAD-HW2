"""Templating URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.ExampleView.as_view(), name='start'),
    url(r'^bullets/', views.BulletsView.as_view(), name='bullets'),
    url(r'^bullet/(?P<id>\d+)', views.BulletView.as_view(), name='bullet_url'),
    url(r'^users/', views.UsersView.as_view(), name='users'),
    url(r'^user/(?P<id>\d+)/$', views.UserView.as_view(), name='user_url'),
    url(
       r'^user/(?P<id>\d+)/follows/(?P<fid>\d+)$',
       views.user_follows,
       name='user_flw'),
    url(
       r'^user/(?P<id>\d+)/unfollows/(?P<fid>\d+)$',
       views.user_unfollows,
       name='user_uflw'),
    url(r'^signup/', views.registration, name='signup'),
    url(r'^post_bullet/', views.post_bullet, name='post_bullet'),
    url(r'^login/', views.authorization, name='login'),
    url(r'^logout/', views.exit, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

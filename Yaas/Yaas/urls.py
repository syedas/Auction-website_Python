"""Assignment3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from logic import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^newuser/$', views.newuser),
    url(r'^login/$', views.userlogin),
    url(r'^logout/$', views.logout),

    url(r'^$', views.Auctions),
    url(r'^myauction/$', views.MyAuctions),
    url(r'^allauction/$', views.Auctions),
    url(r'^createauctions/$', views.addAuction),
    url(r'^(?P<action>reset)/*$', views.reset),
    url(r'^editauction/(?P<id>\d+)$', views.editAuction),
    url(r'^myauction/(?P<id>\d+)$', views.single_auction),
    url(r'^deleteauction/(?P<id>\d+)$', views.delete_auction),

    url(r'^editpswd/$', views.editpswd),
    url(r'^editemail/$', views.editemail),
    url(r'^banauction/(?P<id>\d+)$', views.bannedauction),
    url(r'^language/$', views.changeLanguagePage),
    url(r'^language/(?P<lang_code>\w+)$', views.changelanguage),
    url(r'^bid/(?P<id>\d+)$', views.bid_auction),
    url(r'^search/$', views.search),
    url(r'^email/$', views.email),
    url(r'^api/search/auction/', views.search_api),
    url(r'^api/bid/auction/', views.bid_auction_api),




   # url(r'^addAuction/$', views.addAuction),
]



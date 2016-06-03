from django.conf.urls import url
from . import views

app_name = 'bills'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bills/(?P<bill_id>[0-9]+)/$', views.single, name='single'),
    url(r'^search_by_title/', views.search_by_title, name='search_by_title'),
    url(r'^scraper/', views.scraper, name='scraper'),
]

from django.conf.urls import url
from . import views

app_name = 'bills'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about-us/', views.about_us, name='about_us'), 
    url(r'^bill-listing/', views.about_us, name='bill_listing'),
    url(r'^blog/', views.about_us, name='blog'),
    url(r'^contact-us/', views.about_us, name='contact_us'),
    url(r'^bills/(?P<bill_id>[0-9]+)/$', views.single, name='single'),
    url(r'^search_by_title/', views.search_by_title, name='search_by_title'),
    url(r'^scraper/', views.scraper, name='scraper'),
]

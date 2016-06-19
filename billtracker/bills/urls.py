from django.conf.urls import url
from . import views

app_name = 'bills'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about-us/', views.about_us, name='about_us'),
    url(r'^bill-listing/', views.bill_listing, name='bill_listing'),
    url(r'^blog/', views.blog, name='blog'),
    url(r'^contact-us/', views.contact_us, name='contact_us'),
    url(r'^bills/(?P<bill_id>[0-9]+)/$', views.single, name='single'),
    url(r'^bills/(?P<bill_id>[0-9]+)/revision/(?P<rev_id>[0-9]+)/$', views.revision, name='revision'),
    url(r'^search_by_title/', views.search_by_title, name='search_by_title'),
    url(r'^scraper/', views.scraper, name='scraper'),
    url(r'^app/', views.app, name='app'),
]

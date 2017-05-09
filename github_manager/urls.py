from django.conf.urls import url
from django.contrib import admin


from c_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', views.index, name='index'),
    url(r'^next_page$', views.get_next_repo_data, name='next_page'),
    url(r'^search_company/', views.get_user, name='search'),
]

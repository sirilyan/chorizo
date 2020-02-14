from django.conf.urls import url
from chorizo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.login_view, name="login"),
    url(r'^logout$', views.logout_view, name="logout"),
    url(r'^register$', views.register, name="register"),

    url(r'^give_chore$', views.give_chore, name="give_chore"),
    url(r'^(?P<chore_id>[0-9]+)/complete$', views.complete, name="complete"),
    url(r'^(?P<chore_id>[0-9]+)/details$', views.details, name="details")
]

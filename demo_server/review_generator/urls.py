from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReviewGeneratorView.as_view() , name='index'),
    # path("process/", views.process, name='process'),
]
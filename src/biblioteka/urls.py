from django.urls import path

from . import views

app_name = "biblioteka"

urlpatterns = [
    path("borrowers/", views.borrowers, name="borrowers"),
    path("borrowers/new/", views.borrowers_new, name="borrowers_new"),
    path("", views.index, name="index"),
]

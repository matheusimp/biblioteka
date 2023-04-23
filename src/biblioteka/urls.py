from django.urls import path

from . import views

app_name = "biblioteka"

urlpatterns = [
    path("borrowers/list/", views.borrowers_list, name="borrowers/list"),
    path("borrowers/new/", views.borrowers_new, name="borrowers/new"),
    path("", views.index, name="index"),
]

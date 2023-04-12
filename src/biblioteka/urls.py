from django.urls import path

from . import views

app_name = "biblioteka"

urlpatterns = [
    path("", views.index, name="index"),
]

from django.urls import path

from . import views

app_name = "biblioteka"

urlpatterns = [
    path("borrowers/list/", views.borrowers_list, name="borrowers/list"),
    path("borrowers/new/", views.borrowers_new, name="borrowers/new"),
    path("books/list/", views.books_list, name="books/list"),
    path("books/new/", views.books_new, name="books/new"),
    path("loans/list/", views.loans_list, name="loans/list"),
    path("loans/new/<int:book_id>", views.loans_new, name="loans/new"),
    path("loans/return/", views.loans_return, name="loans/return"),
    path("", views.index, name="index"),
]

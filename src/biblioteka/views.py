from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Book, Borrower, CountryState


def is_empty_or_whitespace(text):
    if text == "":
        return True
    if text.isspace():
        return True

    return False


# Create your views here.
def index(request):
    return render(request, "biblioteka/index.html")


def borrowers_list(request):
    borrowers = Borrower.objects.all()
    return render(request, "biblioteka/borrowers/list.html", {"borrowers": borrowers})


def borrowers_new(request):
    if request.method == "GET":
        states = CountryState.objects.all()
        return render(request, "biblioteka/borrowers/new.html", {"states": states})

    elif request.method == "POST":
        borrower = Borrower(
            name=request.POST["name"],
            birthdate=request.POST["birthdate"],
            cpf=request.POST["cpf"],
            phone=request.POST["phone"],
            email=request.POST["email"],
            zip_code=request.POST["zip_code"],
            address=request.POST["address"],
            city=request.POST["city"],
            state=CountryState.objects.get(pk=request.POST["state"]),
        )

        borrower.save()
        messages.add_message(
            request, messages.SUCCESS, "Cliente cadastrado com sucesso"
        )
        return HttpResponseRedirect(reverse("biblioteka:borrowers/list"))


def books_list(request):
    books = Book.objects.all()
    return render(request, "biblioteka/books/list.html", {"books": books})


def books_new(request):
    if request.method == "GET":
        return render(request, "biblioteka/books/new.html")

    elif request.method == "POST":
        book = Book(
            inventory_id=request.POST.get("inventory_id"),
            isbn=request.POST.get("isbn"),
            available=True,
            title=request.POST.get("title"),
            subtitle=request.POST.get("subtitle"),
            author=request.POST.get("author"),
            genre=request.POST.get("genre"),
            description=request.POST.get("description"),
            pages=request.POST.get("pages"),
            language=request.POST.get("language"),
            publisher=request.POST.get("publisher"),
            publication_date=request.POST.get("publication_date"),
        )

        if is_empty_or_whitespace(book.pages):
            book.pages = None
        if is_empty_or_whitespace(book.publication_date):
            book.publication_date = None

        book.save()
        messages.add_message(request, messages.SUCCESS, "Livro cadastrado com sucesso")
        return HttpResponseRedirect(reverse("biblioteka:books/list"))

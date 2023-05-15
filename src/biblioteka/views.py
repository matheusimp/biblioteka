from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Book, Borrower, CountryState


# If it's None, empty ("") or only whitespace (" "), return None
# Otherwise strip leading/trailing space and consecutive spaces and return the string
def sanitize_input(text):
    if text is None or text == "" or text.isspace():
        return None

    # Remove leading/trailing spaces
    text = text.strip()
    # Remove consecutive spaces
    text = " ".join(text.split())

    return text


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
        name = sanitize_input(request.POST.get("name"))
        birthdate = sanitize_input(request.POST.get("birthdate"))
        cpf = sanitize_input(request.POST.get("cpf"))
        phone = sanitize_input(request.POST.get("phone"))
        email = sanitize_input(request.POST.get("email"))
        zip_code = sanitize_input(request.POST.get("zip_code"))
        address = sanitize_input(request.POST.get("address"))
        city = sanitize_input(request.POST.get("city"))
        state = sanitize_input(request.POST.get("state"))

        borrower = Borrower(
            name=name,
            birthdate=birthdate,
            cpf=cpf,
            phone=phone,
            email=email,
            zip_code=zip_code,
            address=address,
            city=city,
            state=CountryState.objects.get(pk=state),
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
        inventory_id = sanitize_input(request.POST.get("inventory_id"))
        isbn = sanitize_input(request.POST.get("isbn"))
        available = True
        title = sanitize_input(request.POST.get("title"))
        subtitle = sanitize_input(request.POST.get("subtitle"))
        author = sanitize_input(request.POST.get("author"))
        genre = sanitize_input(request.POST.get("genre"))
        description = sanitize_input(request.POST.get("description"))
        pages = sanitize_input(request.POST.get("pages"))
        language = sanitize_input(request.POST.get("language"))
        publisher = sanitize_input(request.POST.get("publisher"))
        publication_date = sanitize_input(request.POST.get("publication_date"))

        book = Book(
            inventory_id=inventory_id,
            isbn=isbn,
            available=available,
            title=title,
            subtitle=subtitle,
            author=author,
            genre=genre,
            description=description,
            pages=pages,
            language=language,
            publisher=publisher,
            publication_date=publication_date,
        )

        book.save()
        messages.add_message(request, messages.SUCCESS, "Livro cadastrado com sucesso")
        return HttpResponseRedirect(reverse("biblioteka:books/list"))

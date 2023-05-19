from datetime import timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Book, Borrower, CountryState, Loan, LoanOptions


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

        try:
            borrower.save()
        except ValidationError as validation_error:
            for field, errors in validation_error:
                field_verbose_name = Borrower._meta.get_field(
                    field
                ).verbose_name.capitalize()

                error_message = f"{field_verbose_name}: {' / '.join(errors)}"

                messages.error(request, error_message)
            return HttpResponseRedirect(reverse("biblioteka:borrowers/new"))
        else:
            messages.success(request, "Cliente cadastrado com sucesso")
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

        try:
            book.save()
        except ValidationError as validation_error:
            for field, errors in validation_error:
                field_verbose_name = Book._meta.get_field(
                    field
                ).verbose_name.capitalize()

                error_message = f"{field_verbose_name}: {' / '.join(errors)}"

                messages.error(request, error_message)
            return HttpResponseRedirect(reverse("biblioteka:books/new"))
        else:
            messages.success(request, "Livro cadastrado com sucesso")
            return HttpResponseRedirect(reverse("biblioteka:books/list"))


def loans_list(request):
    loans = Loan.objects.all()
    return render(request, "biblioteka/loans/list.html", {"loans": loans})


def loans_new(request, book_id):
    if request.method == "GET":
        if book_id is None:
            messages.error(request, "Livro não informado")
            return HttpResponseRedirect(reverse("biblioteka:books/list"))

        book = Book.objects.get(pk=book_id)
        if not book.available:
            messages.error(request, "O livro não está disponível")
            return HttpResponseRedirect(reverse("biblioteka:books/list"))

        borrowers = Borrower.objects.all()
        return render(
            request, "biblioteka/loans/new.html", {"book": book, "borrowers": borrowers}
        )

    elif request.method == "POST":
        book = Book.objects.get(pk=book_id)
        if not book.available:
            messages.error(request, "O livro não está disponível para empréstimo")
            return HttpResponseRedirect(reverse("biblioteka:books/list"))

        borrower = sanitize_input(request.POST.get("borrower_id"))

        borrowed_date = timezone.localtime().date()

        loan_period = LoanOptions.objects.first().loan_period
        due_date = borrowed_date + timedelta(days=loan_period)
        while due_date.weekday() in (saturday := 5, sunday := 6):
            due_date = due_date + timedelta(days=1)

        loan = Loan(
            book=book,
            borrower=Borrower.objects.get(pk=borrower),
            borrowed_date=borrowed_date,
            due_date=due_date,
            returned_date=None,
        )

        book.available = False

        try:
            with transaction.atomic():
                loan.save()
                book.save()

        except ValidationError as validation_error:
            for field, errors in validation_error:
                try:
                    field_verbose_name = Loan._meta.get_field(
                        field
                    ).verbose_name.capitalize()
                    error_message = f"{field_verbose_name}: {' / '.join(errors)}"
                except:
                    error_message = f"{' / '.join(errors)}"

                messages.error(request, error_message)
            return HttpResponseRedirect(
                reverse("biblioteka:loans/new", kwargs={"book_id": book_id})
            )
        else:
            messages.success(request, "Empréstimo realizado com sucesso")
            return HttpResponseRedirect(reverse("biblioteka:loans/list"))


def loans_return(request):
    if request.method == "POST":
        loan_id = sanitize_input(request.POST.get("loan_id"))
        loan = Loan.objects.get(pk=loan_id)
        book = loan.book

        loan.returned_date = timezone.localtime().date()

        if loan.is_active():
            messages.error(request, "O livro não está emprestado")
            return HttpResponseRedirect(reverse("biblioteka:loans/list"))

        try:
            with transaction.atomic():
                book.available = True
                loan.save()
                book.save()

        except ValidationError as validation_error:
            for field, errors in validation_error:
                field_verbose_name = Loan._meta.get_field(
                    field
                ).verbose_name.capitalize()

                error_message = f"{field_verbose_name}: {' / '.join(errors)}"

                messages.error(request, error_message)
            return HttpResponseRedirect(reverse("biblioteka:loans/list"))
        else:
            messages.success(request, "Livro devolvido com sucesso")
            return HttpResponseRedirect(reverse("biblioteka:loans/list"))

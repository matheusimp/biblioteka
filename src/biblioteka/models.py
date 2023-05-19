import string

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def validate_not_empty(text):
    if len(text.strip()) == 0:
        raise ValidationError("Este campo não pode estar vazio")


def validate_no_whitespace(text):
    trimmed_text = "".join(text.split())

    if trimmed_text != text:
        raise ValidationError(f"Este campo não pode conter espaço")


def validate_no_leading_trailing_consecutive_whitespace(text):
    trimmed_text = text.strip()
    trimmed_text = " ".join(trimmed_text.split())

    if trimmed_text != text:
        raise ValidationError(
            "Este campo não pode começar/terminar com espaço ou conter espaços consecutivos"
        )


def validate_only_digits(text):
    for char in text:
        if char not in string.digits:
            raise ValidationError(f"Este campo deve conter somente dígitos")


def validate_date_not_in_future(date):
    today = timezone.localtime().date()

    if date > today:
        raise ValidationError(
            f"Data informada ({date}) não pode ser maior que a data atual ({today})"
        )


def validate_date_at_least_1900(date):
    date_1900_01_01 = parse_datetime("1900-01-01").date()

    if date < date_1900_01_01:
        raise ValidationError(
            f"Data informada ({date}) não pode ser menor que {date_1900_01_01}"
        )


# Create your models here.
class CountryState(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "estado"

    state = models.CharField("estado", max_length=100, unique=True)
    abbreviation = models.CharField("sigla", max_length=2, unique=True)


class Borrower(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "cliente"

    name = models.CharField(
        "nome",
        max_length=255,
        validators=[
            validate_not_empty,
            validate_no_leading_trailing_consecutive_whitespace,
        ],
    )
    birthdate = models.DateField(
        "data de nascimento",
        validators=[validate_date_not_in_future, validate_date_at_least_1900],
    )
    cpf = models.CharField(
        "CPF",
        max_length=11,
        unique=True,
        validators=[
            validate_not_empty,
            validate_no_whitespace,
            validate_only_digits,
            MinLengthValidator(11, "CPF deve conter 11 dígitos"),
        ],
    )
    phone = models.CharField(
        "celular",
        max_length=20,
        validators=[
            validate_not_empty,
            validate_no_whitespace,
            validate_only_digits,
            MinLengthValidator(
                10, "Telefone deve conter no mínimo 10 dígitos (incluindo DDD)"
            ),
        ],
    )
    email = models.EmailField("email", blank=True, default=None, null=True)
    zip_code = models.CharField(
        "cep",
        max_length=8,
        validators=[
            validate_not_empty,
            validate_no_whitespace,
            validate_only_digits,
            MinLengthValidator(8, "CEP deve conter 8 dígitos"),
        ],
    )
    address = models.CharField(
        "endereço",
        max_length=255,
        validators=[
            validate_not_empty,
            validate_no_leading_trailing_consecutive_whitespace,
        ],
    )
    city = models.CharField(
        "cidade",
        max_length=100,
        validators=[
            validate_not_empty,
            validate_no_leading_trailing_consecutive_whitespace,
        ],
    )
    state = models.ForeignKey(
        CountryState, on_delete=models.PROTECT, verbose_name="estado"
    )


class Book(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def validate_10_or_13_characters(text):
        if len(text) != 10 and len(text) != 13:
            raise ValidationError(f"ISBN deve conter 10 ou 13 dígitos")

    def is_borrowed(self):
        active_loan = Loan.objects.filter(book=self.id).filter(
            returned_date__isnull=True
        )

        return active_loan.exists()

    class Meta:
        verbose_name = "livro"

    inventory_id = models.CharField(
        "ID do estoque", max_length=100, unique=True, validators=[validate_not_empty]
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        validators=[
            validate_not_empty,
            validate_no_whitespace,
            validate_only_digits,
            validate_10_or_13_characters,
            MinLengthValidator(10, "ISBN deve conter no mínimo 10 dígitos"),
        ],
    )
    available = models.BooleanField("disponível", default=True)
    title = models.CharField(
        "título",
        max_length=255,
        validators=[
            validate_not_empty,
            validate_no_leading_trailing_consecutive_whitespace,
        ],
    )
    subtitle = models.CharField(
        "subtítulo",
        max_length=255,
        blank=True,
        default=None,
        null=True,
        validators=[validate_no_leading_trailing_consecutive_whitespace],
    )
    author = models.CharField(
        "autor",
        max_length=255,
        blank=True,
        default=None,
        null=True,
        validators=[validate_no_leading_trailing_consecutive_whitespace],
    )
    genre = models.CharField(
        "gênero",
        max_length=255,
        blank=True,
        default=None,
        null=True,
        validators=[validate_no_leading_trailing_consecutive_whitespace],
    )
    description = models.TextField(
        "descrição",
        max_length=1000,
        blank=True,
        default=None,
        null=True,
        validators=[validate_no_leading_trailing_consecutive_whitespace],
    )
    pages = models.IntegerField("páginas", blank=True, default=None, null=True)
    language = models.CharField(
        "idioma",
        max_length=100,
        blank=True,
        default=None,
        null=True,
        validators=[validate_no_leading_trailing_consecutive_whitespace],
    )
    publisher = models.CharField(
        "editora",
        max_length=255,
        blank=True,
        default=None,
        null=True,
        validators=[validate_no_leading_trailing_consecutive_whitespace],
    )
    publication_date = models.DateField(
        "data de publicação", blank=True, default=None, null=True
    )


class LoanOptions(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "opções de empréstimo"

    loan_period = models.IntegerField("prazo de empréstimo")


class Loan(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "empréstimo"
        constraints = [
            UniqueConstraint(
                name="one_active_loan_per_book",
                fields=["book"],
                condition=Q(returned_date=None),
            )
        ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="livro")
    borrower = models.ForeignKey(
        Borrower, on_delete=models.PROTECT, verbose_name="cliente"
    )
    borrowed_date = models.DateField(
        "data de locação", validators=[validate_date_not_in_future]
    )
    due_date = models.DateField("prazo de devolução")
    returned_date = models.DateField(
        "data de devolução",
        blank=True,
        null=True,
        validators=[validate_date_not_in_future],
    )

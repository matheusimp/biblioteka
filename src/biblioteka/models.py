from django.db import models


# Create your models here.
class CountryState(models.Model):
    class Meta:
        verbose_name = "estado"

    state = models.CharField("estado", max_length=100, unique=True)
    abbreviation = models.CharField("sigla", max_length=2, unique=True)


class Borrower(models.Model):
    class Meta:
        verbose_name = "cliente"

    name = models.CharField("nome", max_length=255)
    birthdate = models.DateField("data de nascimento")
    cpf = models.CharField("CPF", max_length=11, unique=True)
    phone = models.CharField("celular", max_length=20)
    email = models.EmailField("email", blank=True, default=None, null=True)
    zip_code = models.CharField("cep", max_length=8)
    address = models.CharField("endereço", max_length=255)
    city = models.CharField("cidade", max_length=100)
    state = models.ForeignKey(
        CountryState, on_delete=models.PROTECT, verbose_name="estado"
    )


class Book(models.Model):
    class Meta:
        verbose_name = "livro"

    inventory_id = models.CharField("ID do estoque", unique=True)
    isbn = models.CharField("ISBN", max_length=13)
    available = models.BooleanField("disponível", default=True)
    title = models.CharField("título", max_length=255)
    subtitle = models.CharField(
        "subtítulo", max_length=255, blank=True, default=None, null=True
    )
    author = models.CharField(
        "autor", max_length=255, blank=True, default=None, null=True
    )
    genre = models.CharField(
        "gênero", max_length=255, blank=True, default=None, null=True
    )
    description = models.TextField(
        "descrição", max_length=1000, blank=True, default=None, null=True
    )
    pages = models.IntegerField("páginas", blank=True, default=None, null=True)
    language = models.CharField(
        "idioma", max_length=100, blank=True, default=None, null=True
    )
    publisher = models.CharField(
        "editora", max_length=255, blank=True, default=None, null=True
    )
    publication_date = models.DateField(
        "data de publicação", blank=True, default=None, null=True
    )

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

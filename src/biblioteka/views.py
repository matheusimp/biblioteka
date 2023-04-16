from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Borrower, CountryState


# Create your views here.
def index(request):
    return render(request, "biblioteka/index.html")


def borrowers(request):
    if request.method == "POST":
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

        return HttpResponseRedirect(reverse("biblioteka:borrowers_new"))


def borrowers_new(request):
    states = CountryState.objects.all()
    return render(request, "biblioteka/borrowers/new.html", {"states": states})

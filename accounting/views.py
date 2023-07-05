from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounting.models import Customers
from django.contrib import messages
from accounting.forms import CustomerForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse


@login_required(login_url="user:login")
def customers(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_customers = Customers.objects.filter(company__contains=keyword)
        return render(request, "customers.html", {"all_customers": all_customers})

    all_customers = Customers.objects.all()

    return render(request, "customers.html", {"all_customers": all_customers})


@login_required(login_url="user:login")
def customer_detail(request, id):
    customer = get_object_or_404(Customers, id=id)

    return render(request, "customer_detail.html", {"customer_detail": customer})


@login_required(login_url="user:login")
def add_customer(request):
    form = CustomerForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        customer = form.save(commit=False)  # creates only the article object
        # customer.company = request.user
        customer.save()
        messages.success(request, "Successfully added a new customer.")

        return redirect("accounting:customers")
    else:
        context = {
            "form": form
        }
        return render(request, "addcustomer.html", context)


@login_required(login_url="user:login")
def update_customer(request, id):
    customer = get_object_or_404(Customers, id=id)
    form = CustomerForm(request.POST or None, request.FILES or None, instance=customer)
    if request.POST and form.is_valid:
        customer = form.save(commit=False)
        customer.author = request.user
        customer.save()
        messages.success(request, "Customer has been successfully updated.")
        return redirect("accounting:customers")

    return render(request, "customer_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_customer(request, id):
    article = get_object_or_404(Customers, id=id)
    article.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:customers")

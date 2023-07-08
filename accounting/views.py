from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounting.models import Customer, BankAccount, Contract
from django.contrib import messages
from accounting.forms import CustomerForm, BankAccountForm, ContractForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse


@login_required(login_url="user:login")
def customers(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_customers = Customer.objects.filter(company__contains=keyword)
        return render(request, "customers.html", {"all_customers": all_customers})

    all_customers = Customer.objects.all()

    return render(request, "customers.html", {"all_customers": all_customers})


@login_required(login_url="user:login")
def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)

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
    customer = get_object_or_404(Customer, id=id)
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
    article = get_object_or_404(Customer, id=id)
    article.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:customers")


# bank accounts
@login_required(login_url="user:login")
def add_bank_account(request):
    form = BankAccountForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        bank_account = form.save(commit=False)  # creates only the article object
        bank_account.save()
        messages.success(request, "Successfully added a new bank account.")

        return redirect("accounting:bank_accounts")
    else:
        context = {
            "form": form
        }
        return render(request, "add_bank_account.html", context)


@login_required(login_url="user:login")
def bank_accounts(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_bank_accounts = BankAccount.objects.filter(account_alias__contains=keyword)
        return render(request, "bank_accounts.html", {"bank_accounts": all_bank_accounts})

    all_bank_accounts = BankAccount.objects.all()

    return render(request, "bank_accounts.html", {"bank_accounts": all_bank_accounts})


@login_required(login_url="user:login")
def bank_account_detail(request, id):
    bank_account = get_object_or_404(BankAccount, id=id)

    return render(request, "bank_account_detail.html", {"bank_account_detail": bank_account})


@login_required(login_url="user:login")
def update_bank_account(request, id):
    bank_account = get_object_or_404(BankAccount, id=id)
    form = BankAccountForm(request.POST or None, request.FILES or None, instance=bank_account)
    if request.POST and form.is_valid:
        bank_account = form.save(commit=False)
        bank_account.save()
        messages.success(request, "Bank account has been successfully updated.")
        return redirect("accounting:bank_accounts")

    return render(request, "bank_account_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_bank_account(request, account_id):
    bank_account = get_object_or_404(BankAccount, id=account_id)
    bank_account.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:bank_accounts")


""" Contracts """


@login_required(login_url="user:login")
def add_contract(request):
    form = ContractForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        contract = form.save(commit=False)  # creates only the article object
        contract.save()
        messages.success(request, "Successfully added a new contract.")

        return redirect("accounting:contracts")
    else:
        context = {
            "form": form
        }
        return render(request, "add_contract.html", context)


@login_required(login_url="user:login")
def contracts(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_contracts = Contract.objects.filter(description__contains=keyword)
        return render(request, "contracts.html", {"contracts": all_contracts})

    all_contracts = Contract.objects.all()

    return render(request, "contracts.html", {"contracts": all_contracts})


@login_required(login_url="user:login")
def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)

    return render(request, "contract_detail.html", {"contract_detail": contract})


@login_required(login_url="user:login")
def update_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    form = ContractForm(request.POST or None, request.FILES or None, instance=contract)
    if request.POST and form.is_valid:
        contract = form.save(commit=False)
        contract.save()
        messages.success(request, "Contract has been successfully updated.")
        return redirect("accounting:contracts")

    return render(request, "contract_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    contract.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:contracts")

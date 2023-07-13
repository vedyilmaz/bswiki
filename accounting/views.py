from datetime import datetime
from random import random

from django.forms import forms, ModelForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounting.models import Customer, BankAccount, Contract, ContractSale
from django.contrib import messages
from accounting.forms import CustomerForm, BankAccountForm, ContractForm, ContractSaleForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

CS_ID = 0
WORKED_HOURS = 0


@login_required(login_url="user:login")
def customers(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_customers = Customer.objects.filter(company__contains=keyword)
        return render(request, "accounting/customers.html", {"all_customers": all_customers})

    all_customers = Customer.objects.all()

    return render(request, "accounting/customer/customers.html", {"all_customers": all_customers})


@login_required(login_url="user:login")
def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)

    return render(request, "accounting/customer/customer_detail.html", {"customer_detail": customer})


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
        return render(request, "accounting/customer/addcustomer.html", context)


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

    return render(request, "accounting/customer/customer_update.html", {"form": form})


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
        return render(request, "accounting/bank_account/add_bank_account.html", context)


@login_required(login_url="user:login")
def bank_accounts(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_bank_accounts = BankAccount.objects.filter(account_alias__contains=keyword)
        return render(request, "accounting/bank_account/bank_accounts.html", {"bank_accounts": all_bank_accounts})

    all_bank_accounts = BankAccount.objects.all()

    return render(request, "accounting/bank_account/bank_accounts.html", {"bank_accounts": all_bank_accounts})


@login_required(login_url="user:login")
def bank_account_detail(request, id):
    bank_account = get_object_or_404(BankAccount, id=id)

    return render(request, "accounting/bank_account/bank_account_detail.html", {"bank_account_detail": bank_account})


@login_required(login_url="user:login")
def update_bank_account(request, id):
    bank_account = get_object_or_404(BankAccount, id=id)
    form = BankAccountForm(request.POST or None, request.FILES or None, instance=bank_account)
    if request.POST and form.is_valid:
        bank_account = form.save(commit=False)
        bank_account.save()
        messages.success(request, "Bank account has been successfully updated.")
        return redirect("accounting:bank_accounts")

    return render(request, "accounting/bank_account/bank_account_update.html", {"form": form})


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
        return render(request, "accounting/contract/add_contract.html", context)


@login_required(login_url="user:login")
def contracts(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_contracts = Contract.objects.filter(description__contains=keyword)
        return render(request, "accounting/contract/contracts.html", {"contracts": all_contracts})

    all_contracts = Contract.objects.all()

    return render(request, "accounting/contract/contracts.html", {"contracts": all_contracts})


@login_required(login_url="user:login")
def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)

    return render(request, "accounting/contract/contract_detail.html", {"contract_detail": contract})


@login_required(login_url="user:login")
def update_contract(request, id):
    contract = get_object_or_404(Contract, id=id)
    form = ContractForm(request.POST or None, request.FILES or None, instance=contract)
    if request.POST and form.is_valid:
        contract = form.save(commit=False)
        contract.save()
        messages.success(request, "Contract has been successfully updated.")
        return redirect("accounting:contracts")

    return render(request, "accounting/contract/contract_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    contract.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:contracts")


@login_required(login_url="user:login")
# @csrf_protect
@csrf_exempt
# @ensure_csrf_cookie
def add_contract_sale(request):

    global CS_ID
    global WORKED_HOURS
    form = ContractSaleForm(request.POST or None, request.FILES or None)
    print("adding a new contract sale record...")

    if form.is_valid():
        print("adding a new contract sale record...")
        contract_sale = form.save(commit=False)  # creates only the contract sale object
        contract_sale.save()
        messages.success(request, "Successfully added a new contract sale.")

        return redirect("accounting:contract_sales")
    else:
        print("form not valid!")
        print("-------")
        print(f"CSID: {CS_ID}")
        print(f"Worked Hours: {WORKED_HOURS}")
        if CS_ID and int(CS_ID) > 0:
            contract_params = Contract.objects.filter(id=CS_ID).values('rate_amount', 'currency')
            if contract_params:

                rate_amount = contract_params[0]['rate_amount']
                currency = contract_params[0]['currency']
                print(f"contract id: {CS_ID}, rate amount:{rate_amount}, currency: {currency}")
                formc = ContractSaleForm(initial={"total_amount": float(rate_amount) * float(WORKED_HOURS),
                                                  "rate_amount": float(rate_amount)})

                context = {
                    "form": formc
                }

                return render(request, "accounting/contract_sale/add_contract_sale.html", context)

        print("rendering not triggered....")
        print(str(datetime.now()))
        form = ContractSaleForm(initial={"rate_amount": random()})

        context = {
            "form": form
        }

        return render(request, "accounting/contract_sale/add_contract_sale.html", context)


def test(request, context):
    print("test...")
    return render(request, "accounting/contract_sale/add_contract_sale.html", context)


@login_required(login_url="user:login")
def contract_sales(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_contracts_sales = ContractSale.objects.filter(description__contains=keyword)
        return render(request, "accounting/contract_sale/contract_sales.html", {"contract_sales": all_contracts_sales})

    # all_contracts_sales = ContractSale.objects.all()
    all_contracts_sales = ContractSale.objects.all().values('id', 'contract', 'date', 'worked_hours', 'total_amount',
                                                            'contract__rate_amount', 'contract__contract_alias',
                                                            'contract__currency')

    context = {
        "contract_sales": all_contracts_sales,
    }
    # BelongsTo.objects.all().values('user', 'team__team_name', 'schedule')
    return render(request, "accounting/contract_sale/contract_sales.html", context)


@login_required(login_url="user:login")
def contract_sale_detail(request, id):

    # print(f"contract sale id:{id}")
    # contract_sale = get_object_or_404(ContractSale, id=id)

    contract_sale = ContractSale.objects.filter(id=id).values('id', 'contract', 'date', 'worked_hours',
                                                              'total_amount', 'contract__rate_amount',
                                                              'contract__contract_alias', 'contract__currency')

    return render(request, "accounting/contract_sale/contract_sale_detail.html", {"contract_sale": contract_sale[0]})


@login_required(login_url="user:login")
def update_contract_sale(request, id):
    contract_sale = get_object_or_404(ContractSale, id=id)
    form = ContractSaleForm(request.POST or None, request.FILES or None, instance=contract_sale)
    if request.POST and form.is_valid:
        contract_sale = form.save(commit=False)
        contract_sale.save()
        messages.success(request, "Contract sale has been successfully updated.")
        return redirect("accounting:contract_sales")

    return render(request, "accounting/contract_sale/contract_sale_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_contract_sale(request, id):
    contract_sale = get_object_or_404(ContractSale, id=id)
    contract_sale.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:contract_sales")


@login_required(login_url="user:login")
def selected_contract_id(request):
    global CS_ID
    global WORKED_HOURS
    CS_ID = 0
    WORKED_HOURS = 0
    if request.method == 'POST':
        CS_ID = request.POST.get('cs_id')
        WORKED_HOURS = request.POST.get('worked_hours') or 0
        print(f"received contract id:{CS_ID}")
        add_contract_sale(request)
        return HttpResponse(HttpResponse.status_code)

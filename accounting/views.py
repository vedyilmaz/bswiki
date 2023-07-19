import json
from datetime import datetime
from random import random

from django.core.files.storage import FileSystemStorage
from django.forms import forms, ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounting.models import Customer, BankAccount, Contract, ContractSale, ContractSalesTransaction
from django.contrib import messages
from accounting.forms import CustomerForm, BankAccountForm, ContractForm, ContractSaleForm, \
                             ContractSalesInvoice, ContractSaleInvoiceForm, ContractSaleTransactForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

CS_ID = 0
WORKED_HOURS = 0


@login_required(login_url="user:login")
def customers(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_customers = Customer.objects.filter(company__contains=keyword)
        return render(request, "accounting/customer/customers.html", {"all_customers": all_customers})

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
        all_contracts = Contract.objects.filter(contract_alias__contains=keyword)
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


# @csrf_protect
# @csrf_exempt
# @ensure_csrf_cookie
@login_required(login_url="user:login")
def add_contract_sale(request):

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
        context = {
            "form": form
        }

        return render(request, "accounting/contract_sale/add_contract_sale.html", context)


@login_required(login_url="user:login")
def contract_sales(request):
    keyword = request.GET.get("keyword")
    if keyword:
        all_contracts_sales = ContractSale.objects.filter(contract__contract_alias__contains=keyword)\
            .values('id', 'contract', 'date', 'worked_hours', 'is_invoiced',
                    'total_amount', 'contract__rate_amount',
                    'contract__contract_alias', 'contract__currency')

        return render(request, "accounting/contract_sale/contract_sales.html", {"contract_sales": all_contracts_sales})

    # all_contracts_sales = ContractSale.objects.all()
    all_contracts_sales = ContractSale.objects.all().values('id', 'contract', 'date', 'worked_hours', 'total_amount',
                                                            'is_invoiced','contract__rate_amount', 'contract__contract_alias',
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
def load_contract(request):
    contract_id = request.GET.get('contract')
    # print(f"contract: {contract}")
    # contract_data = Contract.objects.filter(id=contract)
    # print(f"data:{contract_data}")
    # return render(request, 'accounting/contract_sale/add_contract_sale.html', {'contract': contract_data})
    contract_data = Contract.objects.filter(id=contract_id).values('id', 'contract_alias', 'rate_amount',
                                                                   'currency')

    print(f"contract id: {contract_id}, contract data: {contract_data[0]}")
    # return render(request, 'accounting/contract_sale/add_contract_sale.html', {'contract': contract_data})
    return HttpResponse(json.dumps(contract_data[0]))


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


"""contract sale invoice"""


@login_required(login_url="user:login")
def add_contract_sale_invoice(request):

    form = ContractSaleInvoiceForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        print("adding a new contract sale invoice record...")
        contract_sale_invoice = form.save(commit=False)  # creates only the contract sale invoice object
        contract_sale_invoice.save()

        messages.success(request, "Successfully added a new contract sale invoice.")

        return redirect("accounting:cont_sale_invoices")
    else:
        print("form not valid!")
        invoice_data = request.session.get('selected_invoice_data')

        if invoice_data:

            invoice_data = json.loads(invoice_data)
            context = {
                "form": form,
                "invoice_data": invoice_data,
            }

            print(f"form not valid! saved invoice data: {invoice_data}")

        else:
            context = {
                "form": form,
            }

        return render(request, "accounting/contract_sales_invoice/add_cont_sale_invoice.html", context)


def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url="user:login")
def contract_sale_invoices(request):
    keyword = request.GET.get("keyword")
    if keyword:
        contracts_sales_invoices = ContractSalesInvoice.objects.filter(sales__contract__contract_alias__contains=keyword).\
            values('id', 'sales', 'invoice_number', 'date',
                   'due_date', 'is_paid_off',
                   'sales__contract__contract_alias',
                   'sales__contract__currency',
                   'sales__contract__id',
                   'sales__total_amount')
        return render(request, "accounting/contract_sales_invoice/cont_sale_invoices.html",
                      {"cont_sales_invoices": contracts_sales_invoices})

    # all_contracts_sales = ContractSale.objects.all()
    contracts_sales_invoices = ContractSalesInvoice.objects.all().values('id', 'sales', 'invoice_number', 'date',
                                                                         'due_date', 'is_paid_off',
                                                                         'sales__contract__contract_alias',
                                                                         'sales__contract__currency',
                                                                         'sales__contract__id',
                                                                         'sales__total_amount')

    context = {
        "cont_sales_invoices": contracts_sales_invoices,
    }
    # BelongsTo.objects.all().values('user', 'team__team_name', 'schedule')
    return render(request, "accounting/contract_sales_invoice/cont_sale_invoices.html", context)


@login_required(login_url="user:login")
def cont_sale_invoice_detail(request, id):

    # print(f"contract sale id:{id}")
    # contract_sale = get_object_or_404(ContractSale, id=id)

    contract_sale_invoice = ContractSalesInvoice.objects.filter(id=id).values('id', 'sales', 'invoice_number',
                                                                              'date', 'due_date', 'invoice_file',
                                                                              'sales__contract__contract_alias',
                                                                              'sales__contract__currency',
                                                                              'sales__id',
                                                                              'sales__total_amount')

    # print(f"contract invoice data: {contract_sale_invoice}")
    return render(request, "accounting/contract_sales_invoice/cont_sale_invoice_detail.html",
                  {"cont_sale_invoice": contract_sale_invoice[0]})


@login_required(login_url="user:login")
def update_cont_sale_invoice(request, id):
    contract_sale_invoice = get_object_or_404(ContractSalesInvoice, id=id)
    form = ContractSaleInvoiceForm(request.POST or None, request.FILES or None, instance=contract_sale_invoice)
    if request.POST and form.is_valid:
        contract_sale_invoice = form.save(commit=False)
        contract_sale_invoice.save()
        messages.success(request, "Contract sale invoice has been successfully updated.")
        return redirect("accounting:cont_sale_invoices")

    return render(request, "accounting/contract_sales_invoice/cont_sale_invoice_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_cont_sale_invoice(request, id):
    contract_sale_invoice = get_object_or_404(ContractSalesInvoice, id=id)
    contract_sale_invoice.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:cont_sale_invoices")


@login_required(login_url="user:login")
def set_invoice_data(request):
    sales_id = request.POST.get('sales_id')
    if not sales_id:
        print("sales id not received!")
        return HttpResponse(500)

    sales_data = ContractSale.objects.filter(id=sales_id).values('id', 'contract__id',
                                                                 'contract__customer__company',
                                                                 'contract__currency')
    if not sales_data:
        return HttpResponse(500)

    str_data = json.dumps(sales_data[0])
    print(f"str data: {str_data}")
    form = ContractSaleInvoiceForm(request.POST or None, request.FILES or None)

    context = {
        form: form,
        "invoice_data": str_data,
    }

    request.session['selected_invoice_data'] = str_data

    return HttpResponse(str_data)


@login_required(login_url="user:login")
def add_contract_sales_transaction(request):

    form = ContractSaleTransactForm(request.POST or None, request.FILES or None)
    print("adding a new contract sale transaction record...")

    if form.is_valid():
        print("adding a new contract sale transaction record...")
        contract_sale_transaction = form.save(commit=False)  # creates only the contract sale object
        contract_sale_transaction.save()
        messages.success(request, "Successfully added a new contract sale transaction.")

        return redirect("accounting:cont_sales_transactions")
    else:
        print("form not valid!")

        loaded = request.session.get('selected_invoice_data') or None
        if loaded:
            loaded = json.loads(loaded)
            print(f"data: {loaded}")

            context = {
                "form": form,
                "invoice_data": loaded,
            }
        else:
            context = {
                "form": form,
            }

        return render(request, "accounting/contract_sales_transaction/add_cont_sales_transaction.html", context)


@login_required(login_url="user:login")
def contract_sales_transactions(request):
    keyword = request.GET.get("keyword")
    if keyword:
        cont_sales_transactions = ContractSalesTransaction.objects.filter(invoice__invoice_number__contains=keyword).\
            values('id', 'invoice', 'date',
                   'amount', 'bank_account__account_alias',
                   'invoice__invoice_number',
                   'invoice__sales__contract__contract_alias',
                   'invoice__sales__contract__id',
                   'invoice__sales__contract__currency')

        return render(request, "accounting/contract_sales_transaction/cont_sales_transactions.html",
                      {"cont_sales_transactions": cont_sales_transactions})

    # all_contracts_sales = ContractSale.objects.all()
    cont_sales_transactions = ContractSalesTransaction.objects.all().values('id', 'invoice', 'date',
                                                                            'amount', 'bank_account__account_alias',
                                                                            'invoice__invoice_number',
                                                                            'invoice__sales__contract__contract_alias',
                                                                            'invoice__sales__contract__id',
                                                                            'invoice__sales__contract__currency')
    print(cont_sales_transactions)
    context = {
        "cont_sales_transactions": cont_sales_transactions,
    }
    return render(request, "accounting/contract_sales_transaction/cont_sales_transactions.html", context)


@login_required(login_url="user:login")
def set_transaction_data(request):
    invoice_id = request.POST.get('invoice_id')
    if not invoice_id:
        print("invoice id not received!")
        return HttpResponse(500)

    tdata = ContractSalesInvoice.objects.filter(id=invoice_id).values('id', 'invoice_number', 'sales__total_amount',
                                                                      'sales__contract__currency')
    if not tdata:
        return HttpResponse(500)

    str_data = json.dumps(tdata[0])
    print(f"str data: {str_data}")
    form = ContractSaleTransactForm(request.POST or None, request.FILES or None)

    context = {
        form: form,
        "transaction_data": str_data,
    }

    request.session['selected_invoice_data'] = str_data

    return HttpResponse(str_data)

    # return render(request, 'accounting/contract_sales_transaction/add_cont_sales_transaction.html', context)


@login_required(login_url="user:login")
def cont_sales_transaction_detail(request, id):

    # print(f"contract sale id:{id}")
    # contract_sale = get_object_or_404(ContractSale, id=id)

    contract_sale_transaction = ContractSalesTransaction.objects.filter(id=id).values('id',
                                                                                      'date',
                                                                                      'invoice__sales__contract__contract_alias',
                                                                                      'invoice__invoice_number',
                                                                                      'invoice__sales__total_amount',
                                                                                      'invoice__sales__contract__currency',
                                                                                      'invoice__sales__id',
                                                                                      'note')

    print(f"contract invoice data: {contract_sale_transaction}")
    return render(request, "accounting/contract_sales_transaction/cont_sales_transaction_detail.html",
                  {"cont_sales_transaction": contract_sale_transaction[0]})


@login_required(login_url="user:login")
def update_cont_sales_transaction(request, id):
    contract_sale_transaction = get_object_or_404(ContractSalesTransaction, id=id)
    form = ContractSaleTransactForm(request.POST or None, request.FILES or None, instance=contract_sale_transaction)
    if request.POST and form.is_valid:
        contract_sale_transaction = form.save(commit=False)
        contract_sale_transaction.save()
        messages.success(request, "Contract sale transaction has been successfully updated.")
        return redirect("accounting:cont_sales_transactions")

    return render(request, "accounting/contract_sales_transaction/cont_sales_transaction_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_cont_sales_transaction(request, id):
    contract_sale_transaction = get_object_or_404(ContractSalesTransaction, id=id)
    contract_sale_transaction.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:cont_sales_transactions")

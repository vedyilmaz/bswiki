import json
from _decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from accounting.models import Customer, BankAccount, Contract, ContractSale, ContractSalesTransaction, MileStone
from django.contrib import messages
from accounting.forms import CustomerForm, BankAccountForm, ContractForm, ContractSaleForm, \
    ContractSalesInvoice, ContractSaleInvoiceForm, ContractSaleTransactForm, MileStoneForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
import ast
from accounting.serializers import ContractSaleSerializer, ContractSerializer
from django.core.cache import cache


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
        customer.user = request.user
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
        bank_account.user = request.user
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
        contract.user = request.user
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


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def contract_list(request):
    """
    List all contracts
    """
    print("user autenticated!")

    if request.method == 'GET':
        cont = Contract.objects.all()
        cont = ContractSerializer(cont, many=True, context={'request': request})
        print(f"serialized data: {cont}")
        return JsonResponse(cont.data, safe=False)

        # return render(request, "accounting/contract_sale/contract_sales.html",
        #               {'contract_sales': cont})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        cont = ContractSerializer(data=data)
        if cont.is_valid():
            cont.save()
            return JsonResponse(cont.data, status=201)

        return JsonResponse(cont.errors, status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def contractdetail(request, id):
    contract = Contract.objects.get(pk=id)
    serializer = ContractSerializer(contract)
    return JsonResponse(serializer.data)


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

    referer = request.META.get('HTTP_REFERER')
    if not referer:
        raise Http404

    if form.is_valid():
        print("adding a new contract sale record...")
        contract_sale = form.save(commit=False)  # creates only the contract sale object
        contract_sale.user = request.user
        contract_sale.save()
        messages.success(request, "Successfully added a new contract sale.")

        return redirect("accounting:contract_sales")
    else:
        print("form not valid!")
        contract_data = request.session.get('selected_contract_data')
        if contract_data:
            jdata = json.loads(contract_data)

            print(f"contract data: {jdata}")
            context = {
                "form": form,
                "contract_data": jdata
            }
        else:

            context = {
                "form": form
            }

        return render(request, "accounting/contract_sale/add_contract_sale.html", context)


def error_404(request, exception):
    return render(request, 'error_404.html/', status=404)


def error_500(request, exception):
    return render(request, 'error_500.html/', status=500)


@login_required(login_url="user:login")
def set_sales_data(request):
    contract_id = request.POST.get('contract_id')
    print(f"contract_id: {contract_id}")
    if not contract_id:
        print("contract id not received!")
        return HttpResponse(500)

    selected_contract_data = Contract.objects.filter(id=int(contract_id), is_active=True) \
                        .values('id', 'contract_alias',
                                'contract_name',
                                'contract_type__rate_type__rate_type',
                                'contract_type__field_attributes',
                                'contract_type__rate_type__billing_period__billing_period',
                                'rate_amount', 'currency') or None

    if not selected_contract_data:
        return HttpResponse(500)

    print(f"json contract data: {selected_contract_data}")
    str_data = json.dumps(selected_contract_data[0], cls=DecimalEncoder)
    print(f"str data: {str_data}")
    form = ContractSaleForm(request.POST or None, request.FILES or None)

    context = {
        form: form,
        "contract_data": str_data,
    }

    request.session['selected_contract_data'] = str_data

    return HttpResponse(str_data)


@login_required(login_url="user:login")
@renderer_classes([JSONRenderer, TemplateHTMLRenderer])
def contract_sales(request):
    keyword = request.GET.get("keyword")
    if keyword:
        # all_contracts_sales = ContractSale.objects.\
        #     filter(contract__contract_alias__contains=keyword, user=request.user) \
        #     .values('id', 'contract', 'date', 'sales_data', 'is_invoiced',
        #             'total_amount', 'contract__rate_amount',
        #             'contract__contract_alias', 'contract__contract_name',
        #             'contract__contract_type__rate_type__rate_type', 'contract__currency')

        all_contract_sales = ContractSale.objects.filter(contract__contract_alias__contains=keyword,
                                                         user=request.user)
        serialized_data = ContractSerializer(all_contract_sales, many=True)

        return render(request, "accounting/contract_sale/contract_sales.html",
                      context={"contract_sales": serialized_data.data})

    is_all = request.GET.get('is_all') or None
    print(f"filter data state: {is_all}")

    if is_all and int(is_all) == 1:
        print("---showing all records---")
        # cache.clear()
        all_contract_sales = ContractSale.objects.filter(user=request.user)
        serialized_data = ContractSaleSerializer(all_contract_sales, many=True)

        context = {
            "contract_sales": serialized_data.data,
        }

        print(f"filtered data: {context}")

        template = loader.get_template("accounting/contract_sale/contract_sales.html")

        return HttpResponse(template.render(context, request))

        # return render(request, "accounting/contract_sale/contract_sales.html",
        #               context)

        # ContractSale.objects.filter(~Q(contract__rate_type="project_based"))
    else:
        #  by default show only un-invoiced ones
        print("---by default showing un-invoiced ones only!---")

        filtered_contracts_sales = ContractSale.objects.filter(is_invoiced=False, user=request.user)
        serialized = ContractSaleSerializer(filtered_contracts_sales, many=True)

        if not filtered_contracts_sales:
            return render(request, "accounting/contract_sale/contract_sales.html")

        context = {
            "contract_sales": serialized.data,
        }
        print(context)

        return render(request=request,
                      template_name="accounting/contract_sale/contract_sales.html",
                      context=context)

    # list_dict = [obj for obj in all_contracts_sales]
    # for dic in list_dict:
    #     for key, val in dic.items():
    #         print(f'{key}: {val}')

    # BelongsTo.objects.all().values('user', 'team__team_name', 'schedule')
    # content = render_to_string("accounting/contract_sale/contract_sales.html", context)
    # return HttpResponse(content)

    # return JsonResponse(list_dict, safe=False, status=200)

@api_view(['GET'])
# @renderer_classes([JSONRenderer, TemplateHTMLRenderer])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def contractsale_list(request):
    """
    List all contracts
    """
    print("user authenticated!")

    if request.method == 'GET':
        show_all = request.GET.get("is_all") == '1'
        print(f"show all: {show_all}")
        if show_all:
            all_contract_sales = ContractSale.objects.filter(user=request.user)
        else:
            all_contract_sales = ContractSale.objects.filter(user=request.user, is_invoiced=0)

        serializer = ContractSaleSerializer(all_contract_sales, many=True)
        context = {'contract_sales': serializer.data}

        print(f"serialized data: {serializer.data}")

        return Response(data={'contract_sales': serializer.data})
        #

        # return render(request=request,
        #               template_name="accounting/contract_sale/contractsales.html",
        #               context=context)

        # return HttpResponse(content=json.dumps(serializer.data), content_type="application/json")

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        csale = ContractSaleSerializer(data=data)
        if csale.is_valid():
            csale.save()
            return Response(csale.data, status=201)

        return Response(csale.errors, status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def contractsale_detail(request, id):

    contractsale = ContractSale.objects.get(pk=id)
    serializer = ContractSaleSerializer(contractsale)
    return Response(serializer.data)

    # elif request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #     serializer = ContractSaleSerializer(contractsale, data=data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)
    #
    # elif request.method == 'DELETE':
    #     contractsale.delete()
    #     return HttpResponse(status=204)


@login_required(login_url="user:login")
def contract_sale_detail(request, id):
    # print(f"contract sale id:{id}")
    contract_sale = get_object_or_404(ContractSale, id=id)
    contract_sale = ContractSale.objects.filter(id=id).values('id', 'contract', 'date', 'sales_data',
                                                              'total_amount', 'contract__rate_amount',
                                                              'contract__contract_type__rate_type__rate_type',
                                                              'contract__contract_alias', 'contract__currency')

    return render(request, "accounting/contract_sale/contract_sale_detail.html",
                  {"contract_sale": contract_sale[0]})


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

    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return Http404

    if form.is_valid():
        print("adding a new contract sale invoice record...")
        contract_sale_invoice = form.save(commit=False)  # creates only the contract sale invoice object
        contract_sale_invoice.user = request.user
        contract_sale_invoice.save()

        messages.success(request, "Successfully added a new contract sale invoice.")

        return redirect("accounting:cont_sale_invoices")
    else:
        print("form not valid!")
        invoice_data = request.session.get('selected_invoice_data')

        if invoice_data:
            invoice_data = json.loads(str(invoice_data))
            print(f"json invoice data: {invoice_data}")

            context = {
                "form": form,
                "invoice_data": invoice_data,
            }

            print(f"saved invoice data: {invoice_data}")

            return render(request, "accounting/contract_sales_invoice/add_cont_sale_invoice.html", context)

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
        contracts_sales_invoices = ContractSalesInvoice.objects.filter(contract__contract_name__contains=keyword). \
            values('id', 'sales_ids', 'invoice_number', 'date',
                   'due_date', 'is_paid_off',
                   'total_amount',
                   'contract__contract_name',
                   'contract__contract_alias',
                   'contract__currency',
                   'contract__id')
        return render(request, "accounting/contract_sales_invoice/cont_sale_invoices.html",
                      {"cont_sales_invoices": contracts_sales_invoices})

    # all_contracts_sales = ContractSale.objects.all()
    contracts_sales_invoices = ContractSalesInvoice.objects.all().values('id', 'sales_ids',
                                                                         'invoice_number',
                                                                         'date', 'due_date', 'is_paid_off',
                                                                         'total_amount',
                                                                         'contract__contract_name',
                                                                         'contract__contract_alias',
                                                                         'contract__currency',
                                                                         'contract__id')

    context = {
        "cont_sales_invoices": contracts_sales_invoices,
    }
    # BelongsTo.objects.all().values('user', 'team__team_name', 'schedule')
    return render(request, "accounting/contract_sales_invoice/cont_sale_invoices.html", context)


@login_required(login_url="user:login")
def cont_sale_invoice_detail(request, id):
    # print(f"contract sale id:{id}")
    # contract_sale = get_object_or_404(ContractSale, id=id)

    contract_sale_invoice = ContractSalesInvoice.objects.filter(id=id).values('id', 'contract', 'sales_ids',
                                                                              'invoice_number',
                                                                              'total_amount',
                                                                              'is_paid_off',
                                                                              'date', 'due_date', 'invoice_file',
                                                                              'contract__contract_alias',
                                                                              'contract__currency')

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
    print(f"received sales id: {sales_id}")
    if not sales_id:
        print("sales id not received!")
        return HttpResponse(500)

    # sales_id = sales_id.replace("[", "").replace("]", "") .replace('"', '').replace(',', '')
    sales_id = ast.literal_eval(sales_id)
    print(f"new sales id: {sales_id}")
    sales_list = []
    for sid in sales_id:
        sales_data = ContractSale.objects.filter(id=int(sid)).values('id', 'contract__id',
                                                                     'contract__customer__company',
                                                                     'contract__currency',
                                                                     'total_amount') or None
        if not sales_data:
            print(f"skipping contract id: {sid}...")
            continue

        sales_list.append(sales_data[0])

    print(f"sales dict: {sales_list}")

    str_data = json.dumps(list(sales_list), cls=DecimalEncoder)
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
        contract_sale_transaction.user = request.user
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
        cont_sales_transactions = ContractSalesTransaction.objects.filter(invoice__invoice_number__contains=keyword). \
            values('id', 'invoice', 'date',
                   'amount', 'bank_account__account_alias',
                   'invoice__invoice_number',
                   'invoice__contract__contract_alias',
                   'invoice__contract__id',
                   'invoice___contract__currency')

        return render(request, "accounting/contract_sales_transaction/cont_sales_transactions.html",
                      {"cont_sales_transactions": cont_sales_transactions})

    # all_contracts_sales = ContractSale.objects.all()
    cont_sales_transactions = ContractSalesTransaction.objects.all().values('id', 'invoice', 'date',
                                                                            'amount', 'bank_account__account_alias',
                                                                            'invoice__invoice_number',
                                                                            'invoice__contract__contract_alias',
                                                                            'invoice__contract__id',
                                                                            'invoice__contract__currency')
    print(cont_sales_transactions)
    context = {
        "cont_sales_transactions": cont_sales_transactions,
    }
    return render(request, "accounting/contract_sales_transaction/cont_sales_transactions.html", context)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


@login_required(login_url="user:login")
def set_transaction_data(request):
    invoice_id = request.POST.get('invoice_id')
    if not invoice_id:
        print("invoice id not received!")
        return HttpResponse(500)

    print(f"invoice id: {invoice_id}")
    tdata = ContractSalesInvoice.objects.filter(id=invoice_id).values('id', 'invoice_number', 'total_amount',
                                                                      'contract__currency')
    if not tdata:
        return HttpResponse(500)

    str_data = json.dumps(tdata[0], cls=DecimalEncoder)
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
                                                                                      'invoice__contract__contract_alias',
                                                                                      'invoice__invoice_number',
                                                                                      'invoice__total_amount',
                                                                                      'invoice__contract__currency',
                                                                                      'invoice__id',
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


@login_required(login_url="user:login")
def add_milestone(request):
    form = MileStoneForm(request.POST or None, request.FILES or None)
    print("adding a new milestone record...")

    if form.is_valid():
        print("adding a new milestone record...")
        milestone = form.save(commit=False)  # creates only the contract sale object
        milestone.user = request.user
        milestone.save()
        messages.success(request, "Successfully added a new milestone.")

        return redirect("accounting:milestones")
    else:
        print("form not valid!")

        milestone_data = request.session.get('selected_contract_data') or None
        if milestone_data:
            jdata = json.loads(milestone_data)
            print(f"data: {jdata}")

            context = {
                "form": form,
                "milestone_data": jdata,
            }
        else:
            context = {
                "form": form,
            }

        return render(request, "accounting/milestone/add_milestone.html", context)


@login_required(login_url="user:login")
def milestones(request):
    keyword = request.GET.get("keyword")
    if keyword:
        milestones_data = MileStone.objects.filter(contract__contract_alias__contains=keyword). \
            values('id', 'contract', 'due_date', 'delivery_date', 'milestone_number',
                   'is_completed', 'milestone_amount',
                   'contract__contract_alias',
                   'contract__currency',
                   'contract__id')

        return render(request, "accounting/milestone/milestones.html",
                      {"milestone_list": milestones_data})

    milestones_data = MileStone.objects.all(). \
        values('id', 'contract', 'due_date', 'delivery_date', 'milestone_number',
               'is_completed', 'milestone_amount',
               'contract__contract_alias',
               'contract__currency',
               'contract__id')

    context = {
        "milestone_list": milestones_data,
    }
    # BelongsTo.objects.all().values('user', 'team__team_name', 'schedule')
    return render(request, "accounting/milestone/milestones.html", context)


@login_required(login_url="user:login")
def update_milestone(request, id):
    milestone = get_object_or_404(MileStone, id=id)
    form = MileStoneForm(request.POST or None, request.FILES or None, instance=milestone)
    if request.POST and form.is_valid:
        milestone = form.save(commit=False)
        milestone.save()
        messages.success(request, "Milestone has been successfully updated.")
        return redirect("accounting:milestones")

    return render(request, "accounting/milestone/milestone_update.html", {"form": form})


@login_required(login_url="user:login")
def delete_milestone(request, id):
    milestone = get_object_or_404(MileStone, id=id)
    milestone.delete()
    messages.success(request, "Successfully deleted...")
    return redirect("accounting:milestones")


@login_required(login_url="user:login")
def set_milestone_data(request):
    ms_id = request.POST.get('milestone_id')
    print(f"received sales id: {ms_id}")
    if not ms_id:
        print("milestone id not received!")
        return HttpResponse(500)

    milestone_id = ast.literal_eval(ms_id)
    print(f"new sales id: {milestone_id}")
    milestone_list = []
    for sid in milestone_id:
        milestone_data = MileStone.objects.filter(id=int(sid)).\
                             values('id', 'contract',
                                    'due_date', 'delivery_date',
                                    'milestone_number', 'is_completed',
                                    'milestone_amount',
                                    'total_amount') or None
        if not milestone_data:
            print(f"skipping contract id: {sid}...")
            continue

        milestone_list.append(milestone_data[0])

    print(f"milestone dict: {milestone_list}")

    str_data = json.dumps(list(milestone_list), cls=DecimalEncoder)
    print(f"str data: {str_data}")

    form = ContractSaleInvoiceForm(request.POST or None, request.FILES or None)

    context = {
        form: form,
        "milestone_data": str_data,
    }

    request.session['selected_milestone_data'] = str_data

    return HttpResponse(str_data)
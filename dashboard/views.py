from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accessories.models import Product, Sale, Brand, Model
from account.models import MyUser
from django.contrib.auth.models import User
from dashboard.forms import ModelForm, ProductsForm, SaleForm, BrandForm, SearchForm, ReportSearchForm
from dashboard.models import * 
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import datetime
from datetime import datetime, timedelta, date
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.http import HttpResponse
from django.http import JsonResponse
import csv
import decimal
import math
from dateutil.relativedelta import relativedelta

import calendar, datetime

from django.db.models import Sum
from django.shortcuts import render
from django import forms


@login_required
def index(request):
    total_amount = 0
    total_item = 0
    total_Sale_amount = 0
    total_profit = 0
    profit = 0

    product_item = Product.objects.all()
    model_item = Model.objects.all()
    users = MyUser.objects.count()
    total_item = product_item.count()
    low_quantity_products = Product.objects.filter(product_quantity__lt=5).count()
    for product in product_item:
        if product.product_quantity < 5:
            messages.warning(request, f"The quantity of {product.product_name} is less than 5 !")

        profit = product.actual_Sale_price - (product.sale_quantity * product.buying_price)
        total_amount += product.buying_price*product.product_quantity
        total_Sale_amount += product.actual_Sale_price
        total_profit += profit

    context = {
        'users': users,
        'model_item': model_item,
        'product_item' : product_item,
        'total_item': total_item,
        'total_amount': total_amount,
        'total_profit' : total_profit,
        'total_Sale_amount':total_Sale_amount,
        'profit' : profit,
        'low_quantity_products': low_quantity_products
    } 
    return render(request, 'dashboard/index.html', context)


def filter_data(request):
	models =request.GET.getlist('models[]')
	brands=request.GET.getlist('brand[]')
	product = Product.objects.all().order_by('-id').distinct()
	if len(models)>0:
		allProducts=product.filter(category__id__in=models).distinct()
	if len(brands)>0:
		allProducts=product.filter(brand__id__in=brands).distinct()
     
	return render(request, ('datalist.html'), {'allProducts':allProducts})

@login_required
def tables(request):
    total_amount = 0
    total_item = 0
    total_Sale_amount = 0
    profit = 0
    total_profit = 0
   
   # Search
    if 'quary_set' in request.GET:
        quary_set = request.GET['quary_set']
        # product_item = Product.objects.filter(product_name__icontains=quary_set, model_name__icontains=quary_set)
        multiple_q = Q(Q(product_name__icontains=quary_set) | Q(model__icontains=quary_set))
        product_item = Product.objects.filter(multiple_q)
        
    else:
        product_item = Product.objects.all()
        form = SearchForm(request.POST or None)
        context ={
            'form': form,
            'product_item': product_item
        }

        if request.method == 'POST':
            model = form['model'].value()
            if (model != ''):
                product_item = product_item.filter(model_id=model)

        total_item = product_item.count()
        low_quantity_products = Product.objects.filter(product_quantity__lt=5).count()
        for product in product_item:
            if product.product_quantity < 5:
                messages.warning(request, f"The quantity of {product.product_name} is less than 5 !")

            profit = product.actual_Sale_price - product.remining_quantity
            total_amount += product.buying_price*product.product_quantity
            total_Sale_amount += product.actual_Sale_price
            total_profit += profit 

        page = request.GET.get('page', 1)
        paginator = Paginator(product_item, 50)
        try:
            product_item = paginator.page(page)

        except PageNotAnInteger:
            # fall back to first page
            product_item = paginator.page(1)
        except EmptyPage:
            # fall back to last page
            product_item = paginator.page(paginator.num_pages) 
    
    models = Model.objects.all()
    brands = Brand.objects.all()

    context = {
        'form':form,
        'product_item': product_item,
        'total_item': total_item,
        'brands': brands,
        'models': models,
        'total_amount': total_amount,
        'profit' : profit,
        'total_profit' : total_profit,
        'total_Sale_amount': total_Sale_amount,
        'low_quantity_products': low_quantity_products
    }
    return render(request, ['dashboard/tables.html', 'dashboard/index.html'], context)


@login_required
def add_product(request):
    # product_form = ProductsForm()
    # brand_form = BrandForm()
    # model_form = ModelForm()

    # if request.method == 'POST':
    #     if 'add-product' in request.POST:
    #         product_form = ProductsForm(request.POST or None, request.FILES or None)
    #         if product_form.is_valid():
    #             product_form.save()
    #             return redirect('dashboard:tables')
    #         else:
    #             product_form = ProductsForm()
        
    #     if 'add-brand' in request.POST:
    #         brand_form = BrandForm(request.POST or None, request.FILES or None)
    #         if brand_form.is_valid():
    #             brand_form.save()
    #             return redirect('dashboard:add_product')
    #         else:
    #             brand_form = BrandForm()
        
    #     if 'add-model' in request.POST:
    #         model_form = ModelForm(request.POST or None, request.FILES or None)
    #         if model_form.is_valid():
    #             model_form.save()
    #             return redirect('dashboard:add_product')
    #         else:
    #             model_form = ModelForm()
        

    # product_form = ProductsForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()
    #     messages.success(request, "The product has been added successfully!")
    #     return redirect('dashboard:tables')
    # else:
    #     form = ProductsForm()

    # brand_form = ProductsForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()
    #     messages.success(request, "The product has been added successfully!")
    #     return redirect('dashboard:form_basic')
    # else:
    #     form = BrandForm()
        
    # model_form = ProductsForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()
    #     messages.success(request, "The product has been added successfully!")
    #     return redirect('dashboard:form_basic')
    # else:
    #     form = ModelForm()

    form = ProductsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "The brand has been added successfully!")
        return redirect('dashboard:tables')
    else:
        form = ProductsForm()
    context = {
        'form': form,
    }
    return render(request, "dashboard/form_basic.html", context)

@login_required
def add_brand(request):
    form = BrandForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "The brand has been added successfully!")
        return redirect('dashboard:tables')
    else:
        form = BrandForm()
    context = {
        'form': form,
    }
    return render(request, "dashboard/form_brand.html", context)

@login_required
def add_model(request):
    form = ModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "The brand has been added successfully!")
        return redirect('dashboard:tables')
    else:
        form = ModelForm()
    context = {
        'form': form,
    }
    return render(request, "dashboard/form_model.html", context)

@login_required
def upadate_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductsForm(instance=product)
    
    context = {
        "form": form,
    }
    product_inc = Product.objects.get(id=product_id)
    form = ProductsForm(request.POST or None, request.FILES or None, instance=product_inc)
    if form.is_valid():
        form.save()
        return redirect('dashboard:tables')
    else:
        form = ProductsForm()
    return render(request, 'product/update.html', context)


@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, "The product has been delete successfully!")
    return redirect('dashboard:tables')

@login_required
def sale_quantity(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product_id': product_id,
        'product' : product
    }
    return render(request, 'product/sell.html', context)

@login_required
def confirm_Sale(request, product_id):
    try:
        quantity = int(request.POST.get('quantity'))
        sale_price = int(request.POST.get('price'))
        sale = Sale.objects.filter(product_id=product_id).first()
        sale_q = Product.objects.get(id=product_id)
        
        if sale:
            sale.sale_quantity += quantity
            sale.sale_price += sale_price
            sale.total_Sale_price += (sale_price*quantity)
            sale.save()
        else:
            sale = Sale(sale_quantity=quantity, sale_price=sale_price, product=sale_q, sale_at=date.today())
            sale.total_Sale_price = sale_price * quantity
            sale.save()

        if sale_q.product_quantity >= quantity:
            sale_q.product_quantity -= quantity
            sale_q.sale_quantity += quantity
            sale_q.remining_quantity += (sale_q.buying_price*quantity)
            sale_q.actual_Sale_price += (sale_price*quantity)
            sale_q.save()
            return redirect('dashboard:tables')
    except Exception as e:
        print(e)
        raise Exception("Something wrong")


@login_required
def product_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = product.csv'
    writer = csv.writer(response)
    products = Product.objects.all()
    writer.writerow(['Product Name', 'Brand Name', 'Quantity', 'Buying Price', 'Saleing Price', 'Saleing Quantity', 'Total Amount'])
    
    for product in products:  
        writer.writerow([product.product_name, product.model, product.product_quantity, product.buying_price, product.expecting_Saleing_price, product.remining_quantity, product.quantity_update_date, product.remining_quantity_date])
    return response


def daily_report(request):
    pass
    # total = 0
    # total_amount = 0
    # if request.method == 'POST':
    #     from_date = request.POST.get('from_date')
    #     to_date = request.POST.get('to_date')

    #     queryset = Sale.objects.raw('select id, product, sale_quantity, sale_price, total_Sale_price, profit, sale_at, update_at from accessories_sale where sale_at between "'+from_date+'" and "'+to_date+'"')
       
    #     # total = sum(queryset.values_list('sale_quantity',flat=True))
    #     # total_amount = queryset.aggregate(total=Sum('total_Sale_price', flat=True))
    #     return render(request, 'daily_report.html', {'queryset': queryset, 'total_amount':total_amount, 'total':total})
    
    # else:
    #     queryset = Sale.objects.all()
    #     total = sum(queryset.values_list('sale_quantity',flat=True))
    #     total_amount = queryset.aggregate(total=Sum('total_Sale_price', flat=True))
    #     return render(request, 'daily_report.html', {'queryset': queryset, 'total':total, 'total_amount':total_amount})
    
    # form = ReportSearchForm(request.POST or None)
    # if request.method == 'POST':
    #     queryset = Sale.objects.filter(
    #         sale_at__range = [
    #             form['start_date'].value(),
    #             form['end_date'].value()
    #             ],
    #         update_at__range = [
    #             form['start_date'].value(),
    #             form['end_date'].value()
    #             ]
    #     )
        
    #     return render(request, 'daily_report.html', {
    #     'queryset': queryset,
    #     'form': form
    # })
    # else:
    #     queryset = Sale.objects.all()
    
    
    #     return render(request, 'daily_report.html', {
    #     'queryset': queryset,
    #     'form': form
    # })


#Date and Monthwise Report ---Pranab-----

from datetime import datetime
@login_required
def report(request):
    total_amount = 0
    total_profit = 0

    # get the current year and month
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    print("Current year :", current_year)
    print("Current month :", current_month)

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('current_year', current_year)

        print("Month :", month)
        print("Year :", year)

        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        print('from_date : ', from_date)
        print('to_date : ', to_date)

        queryset = Sale.objects.all()

        if month and len(month) == 2:
            queryset = queryset.filter(sale_at__month=month, sale_at__year=year)
        elif from_date and to_date:
            queryset = queryset.filter(sale_at__range=[from_date, to_date])

        total_amount = sum(queryset.values_list('total_Sale_price', flat=True))
        for sale in queryset:
            total_profit += (sale.total_Sale_price - sale.product.buying_price * sale.sale_quantity)

        return render(request, 'dashboard/report.html', {'queryset': queryset, 'total_amount': total_amount, 'total_profit': total_profit})

    else:
        queryset = Sale.objects.all()
        total = sum(queryset.values_list('sale_quantity', flat=True))
        total_amount = sum(queryset.values_list('total_Sale_price', flat=True))

        for sale in queryset:
            total_profit += (sale.total_Sale_price - sale.product.buying_price * sale.sale_quantity)

        return render(request, 'dashboard/report.html', {'queryset': queryset, 'total': total, 'total_amount': total_amount, 'total_profit': total_profit})


    # def report(request, type):
    # values = type.split(',')
    # if type == 'daily':
    # elif type == 'weekly':
    # elif type == 'monthly':
    # context = {
    #     'values': values,
    #     }
    # return render(request, 'dashboard/report.html', context)


from django.db.models.functions import TruncDay, ExtractWeek
from django.db.models import Sum
import json
def chat(request):
    data = Sale.objects.annotate(day=TruncDay('sale_at')).values('day').annotate(sale_quantity=Sum('sale_quantity'))
    
    # Process the data to create a list of labels and data points
    labels = [d['day'].strftime("%B %d") for d in data]
    data_points = [d['sale_quantity'] for d in data]

    # Create the chart data
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Sale Quantity per Day',
            'data': data_points,
            'fill': False,
            'borderColor': 'rgba(255, 99, 132, 1)',
            'lineTension': 0.1
        }]
    }
    chart_data_json = json.dumps(chart_data)

    context = {
        'data_points': data_points,
        'chart_data_json': chart_data_json
    }
    return render(request, "dashboard/chat.html", context)


def summary(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'summary.html', context)

def accessories_summary(request):
    todays_date = datetime.date.today()
    months_ago = todays_date-datetime.timedelta(days=30)
    items = Product.objects.filter(owner=request.user, added_at__gte=months_ago, added_at__lte=todays_date)

    finalrep = {}

    def get_product_item(item):
        return item.product_name
    item_list = list(set(map(get_product_item, items)))
    print(item_list)

    def get_product_quantity(product_quntity):
        product_quntity = 0
        filtered_by_product_quntity = items.filter(product_quntity=product_quntity)

        for p_item in filtered_by_product_quntity:
            product_quntity += p_item.product_quantity

        print(product_quntity)
        return product_quntity

    for x in items:
        for y in item_list:
            finalrep[y] = get_product_quantity(y)
    print(finalrep)

    return JsonResponse({'accessories_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'stats.html')








@login_required
def charts(request):
    return render(request, 'dashboard/charts.html')

@login_required
def widgets(request):
    return render(request, 'dashboard/widgets.html')

@login_required
def grid(request):
    return render(request, "dashboard/grid.html")

@login_required
def form_basic(request):
    return render(request, "dashboard/form_basic.html")

@login_required
def form_wizard(request):
    return render(request, "dashboard/form_wizard.html")

@login_required
def buttons(request):
    return render(request, "dashboard/buttons.html")

@login_required
def icon_material(request):
    return render(request, "dashboard/icon-material.html")

def icon_fontawesome(request):
    return render(request, "dashboard/icon-fontawesome.html")

def elements(request):
    return render(request, "dashboard/elements.html")

def gallery(request):
    return render(request, "dashboard/gallery.html")

def invoice(request):
    return render(request, "dashboard/invoice.html")


from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render

from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


@staff_member_required
def get_filter_options(request):
    grouped_purchases = Sale.objects.annotate(year=ExtractYear("sale_at")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


def get_sales_chart(request, year):
    purchases = Sale.objects.filter(sale_at__year=year)
    grouped_purchases = purchases.annotate(price=F("total_Sale_price")).annotate(month=ExtractMonth("sale_at"))\
        .values("month").annotate(average=Avg("total_Sale_price")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })




def spend_per_customer_chart(request, year):
    purchases = Sale.objects.filter(sale_at__year=year)
    grouped_purchases = purchases.annotate(price=F("total_Sale_price")).annotate(month=ExtractMonth("sale_at"))\
        .values("month").annotate(average=Avg("total_Sale_price")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })


# @staff_member_required
# def payment_success_chart(request, year):
#     purchases = Purchase.objects.filter(time__year=year)

#     return JsonResponse({
#         "title": f"Payment success rate in {year}",
#         "data": {
#             "labels": ["Successful", "Unsuccessful"],
#             "datasets": [{
#                 "label": "Amount ($)",
#                 "backgroundColor": [colorSuccess, colorDanger],
#                 "borderColor": [colorSuccess, colorDanger],
#                 "data": [
#                     purchases.filter(successful=True).count(),
#                     purchases.filter(successful=False).count(),
#                 ],
#             }]
#         },
#     })


# @staff_member_required
# def payment_method_chart(request, year):
#     purchases = Purchase.objects.filter(time__year=year)
#     grouped_purchases = purchases.values("payment_method").annotate(count=Count("id"))\
#         .values("payment_method", "count").order_by("payment_method")

#     payment_method_dict = dict()

#     for payment_method in Purchase.PAYMENT_METHODS:
#         payment_method_dict[payment_method[1]] = 0

#     for group in grouped_purchases:
#         payment_method_dict[dict(Purchase.PAYMENT_METHODS)[group["payment_method"]]] = group["count"]

#     return JsonResponse({
#         "title": f"Payment method rate in {year}",
#         "data": {
#             "labels": list(payment_method_dict.keys()),
#             "datasets": [{
#                 "label": "Amount ($)",
#                 "backgroundColor": generate_color_palette(len(payment_method_dict)),
#                 "borderColor": generate_color_palette(len(payment_method_dict)),
#                 "data": list(payment_method_dict.values()),
#             }]
#         },
#     })


@staff_member_required
def statistics_view(request):
    return render(request, "statistics.html", {})

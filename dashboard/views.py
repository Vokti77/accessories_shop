from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accessories.models import Product, Sell
from dashboard.forms import ProductsForm, SellForm
from dashboard.models import * 
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import datetime
from datetime import datetime, timedelta
from django.http import HttpResponse
import csv
import decimal
import math

@login_required
def index(request):
    total_quantity = 0
    total_amount = 0
    total_sell_amount = 0
    total_profit = 0
    total_sold = 0
    profit = 0
    product_item = Product.objects.all()
    for product in product_item:
        total_quantity += product.product_quantity
        profit = product.actual_sell_price - (product.sale_quantity * product.buying_price)
        total_amount += product.buying_price*product.product_quantity
        total_sell_amount += product.actual_sell_price
        total_sold += product.sale_quantity
        total_profit += profit
    context = {
        'product_item' : product_item,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
        'total_profit' : total_profit,
        'total_sold' : total_sold,
        'total_sell_amount':total_sell_amount,
        'profit' : profit,
    } 
    return render(request, 'dashboard/index.html', context)


@login_required
def tables(request):
    total_quantity = 0
    total_amount = 0
    total_sell_amount = 0
    profit = 0
    total_profit = 0
    total_sold = 0
    if 'quary_set' in request.GET:
        quary_set = request.GET['quary_set']
        # product_item = Product.objects.filter(product_name__icontains=quary_set, brand_name_name__icontains=quary_set)
        multiple_q = Q(Q(product_name__icontains=quary_set) | Q(brand_name__icontains=quary_set))
        product_item = Product.objects.filter(multiple_q)
        
    else:
        product_item = Product.objects.all()
        for product in product_item:
            if product.product_quantity < 5:
                messages.warning(request, f"The quantity of {product.product_name} is less than 5.")

            total_quantity += product.product_quantity
            profit = product.actual_sell_price - (product.sale_quantity * product.buying_price)
            total_amount += product.buying_price*product.product_quantity
            total_sell_amount += product.actual_sell_price
            total_sold += product.sale_quantity
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

    if product.product_quantity < 5:
        messages.warning(request, f"The quantity of {product.product_name} is less than 5.")
        
    context = {
        'product_item' : product_item,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
        'profit' : profit,
        'total_profit' : total_profit,
        'total_sold' : total_sold,
        'total_sell_amount':total_sell_amount
    }
    return render(request, ['dashboard/tables.html', 'dashboard/index.html'], context)


@login_required
def add_product(request):
    form = ProductsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:add-product')
    else:
        form = ProductsForm()
    context = {
        'form': form,
    }
    return render(request, "dashboard/form_basic.html", context)


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
    return redirect('dashboard:tables')

@login_required
def sell_quantity(request, product_id):
    context = {
        'product_id': product_id,
    }
    return render(request, 'product/sell.html', context)

@login_required
def confirm_sell(request, product_id):
    try:
        quantity = int(request.POST.get('quantity'))
        sell_price = int(request.POST.get('price'))
        # Sell(sell_quantity = quantity, actual_sell_price = sell_price).save()
        sell_q = Product.objects.get(id=product_id)
        sale = Sell.objects.filter(product_id=product_id).first()
        if sale:
            sale.sell_quantity += quantity
            sale.sell_price += (sell_price*quantity)
            sale.save()
        else:
            Sell(sell_quantity=quantity, sell_price=sell_price, product=sell_q).save()

        if sell_q.product_quantity >= quantity:
            sell_q.product_quantity -= quantity
            sell_q.sale_quantity += quantity
            sell_q.remining_quantity = sell_price
            sell_q.actual_sell_price += (sell_price*quantity)
            sell_q.save()
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
    writer.writerow(['Product Name', 'Brand Name', 'Quantity', 'Buying Price', 'Selling Price', 'Selling Quantity', 'Total Amount'])
    
    for product in products:  
        writer.writerow([product.product_name, product.brand_name, product.product_quantity, product.buying_price, product.expecting_selling_price, product.remining_quantity, product.quantity_update_date, product.remining_quantity_date])
    return response


@login_required
def report(request, type):
    values = type.split(',')
    today = datetime.now().date()
    if type == 'daily':
        products = Product.objects.filter(Q(added_at=today) | Q(update_at=today))  #(Q(date_added__gte=week_ago) | Q(date_sold__gte=week_ago)
    elif type == 'weekly':
        week_ago = today - timedelta(days=7)
        products = Product.objects.filter(Q(added_at__range=(week_ago, today)) | Q(update_at__range=(week_ago, today)))
    elif type == 'monthly':
        month_ago = today - timedelta(days=30)
        products = Product.objects.filter(Q(added_at__range=(month_ago, today)) | Q(update_at__range=(month_ago, today)))

    total_quantity = 0
    total_selling_price = 0
    total_buying_price = 0
    total_profit = 0
    total_sold = 0
    profit = 0

    # products = Product.objects.all()
    for product in products:
        total_quantity += product.product_quantity
        total_sold += product.sale_quantity

        total_buying_price +=  product.buying_price * product.product_quantity
    
        total_selling_price += product.expecting_selling_price * product.sale_quantity

        profit = product.actual_sell_price - (product.sale_quantity * product.buying_price)

        total_profit += profit

    context = {
        'total_quantity': total_quantity,
        'total_selling_price': total_selling_price,
        'total_buying_price': total_buying_price,
        'total_profit': total_profit,
        'values': values,
        'products': products,
        'total_sold' : total_sold,

    }


    return render(request, 'dashboard/report.html', context)

from django.db.models.functions import TruncDay, ExtractWeek
from django.db.models import Sum
import json


def chat(request):
    data = Sell.objects.annotate(day=TruncDay('sell_at')).values('day').annotate(sell_quantity=Sum('sell_quantity'))
    
    # Process the data to create a list of labels and data points
    labels = [d['day'].strftime("%B %d") for d in data]
    data_points = [d['sell_quantity'] for d in data]

    # Create the chart data
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Sell Quantity per Day',
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





def calculate_profit(request):
    pass
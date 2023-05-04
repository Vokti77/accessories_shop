from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accessories.models import Product, Sell
from account.models import MyUser
from django.contrib.auth.models import User
from dashboard.forms import ProductsForm, SellForm
from dashboard.models import * 
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import datetime
from datetime import datetime, timedelta, date
from django.http import HttpResponse
from django.http import JsonResponse
import csv
import decimal
import math

@login_required
def index(request):
    total_amount = 0
    total_item = 0
    total_sell_amount = 0
    total_profit = 0
    profit = 0

    product_item = Product.objects.all()
    user = MyUser.objects.count()
    total_item = product_item.count()
    low_quantity_products = Product.objects.filter(product_quantity__lt=5).count()
    for product in product_item:
        if product.product_quantity < 5:
            messages.warning(request, f"The quantity of {product.product_name} is less than 5 !")

        profit = product.actual_sell_price - (product.sale_quantity * product.buying_price)
        total_amount += product.buying_price*product.product_quantity
        total_sell_amount += product.actual_sell_price
        total_profit += profit
    context = {
        'user': user,
        'product_item' : product_item,
        'total_item': total_item,
        'total_amount': total_amount,
        'total_profit' : total_profit,
        'total_sell_amount':total_sell_amount,
        'profit' : profit,
        'low_quantity_products': low_quantity_products
    } 
    return render(request, 'dashboard/index.html', context)


@login_required
def tables(request):
    total_amount = 0
    total_item = 0
    total_sell_amount = 0
    profit = 0
    total_profit = 0
   
    if 'quary_set' in request.GET:
        quary_set = request.GET['quary_set']
        # product_item = Product.objects.filter(product_name__icontains=quary_set, brand_name_name__icontains=quary_set)
        multiple_q = Q(Q(product_name__icontains=quary_set) | Q(brand_name__icontains=quary_set))
        product_item = Product.objects.filter(multiple_q)
        
    else:
        product_item = Product.objects.all()
        total_item = product_item.count()
        low_quantity_products = Product.objects.filter(product_quantity__lt=5).count()
        

        for product in product_item:
            if product.product_quantity < 5:
                messages.warning(request, f"The quantity of {product.product_name} is less than 5 !")

            profit = product.actual_sell_price - product.remining_quantity
            total_amount += product.buying_price*product.product_quantity
            total_sell_amount += product.actual_sell_price
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
        'product_item': product_item,
        'total_item': total_item,
        'total_amount': total_amount,
        'profit' : profit,
        'total_profit' : total_profit,
        'total_sell_amount': total_sell_amount,
        'low_quantity_products': low_quantity_products
    }
    return render(request, ['dashboard/tables.html', 'dashboard/index.html'], context)


@login_required
def add_product(request):
    form = ProductsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "The product has been added successfully!")
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
    messages.success(request, "The product has been delete successfully!")
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
            sale.sell_price += sell_price
            sale.total_sell_price += (sell_price*quantity)
            sale.save()
        else:
            sell = Sell(sell_quantity=quantity, sell_price=sell_price, product=sell_q, sell_at=date.today())
            sell.save()

        if sell_q.product_quantity >= quantity:
            sell_q.product_quantity -= quantity
            sell_q.sale_quantity += quantity
            sell_q.remining_quantity += (sell_q.buying_price*quantity)
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


def daily_report(request):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    # Get the quantities sold for each product on the current day
    today_sales = Sell.objects.filter(Q(sell_at=today) | Q(update_at=today))
    today_quantities = today_sales.values('product', 'product__product_name').annotate(
        total_quantity=Sum('sell_quantity'),
        total_profit=Sum(F('sell_quantity') * (F('sell_price') - F('product__buying_price')))
    ).order_by('product')

    # today_quantities = today_sales.values('product', 'product__product_name', 'product__buying_price').annotate(total_quantity=Sum('sell_quantity')).order_by('product')
   
    # Get the total quantities sold for each product, including previous days
    previous_sales = Sell.objects.filter(Q(sell_at=yesterday) | Q(update_at=yesterday)).values('product').annotate(total_quantity=Sum('sell_quantity')).order_by('product')
    
    # Merge the two querysets to get the updated quantities for each product
    quantities = []
    for today_quantity in today_quantities:
        for previous_quantity in previous_sales:
            if today_quantity['product'] == previous_quantity['product']:
                today_quantity['total_quantity'] += today_quantity['total_quantity']
                break
        quantities.append(today_quantity)

    total_amount = today_sales.aggregate(Sum('sell_price'))['sell_price__sum']
    total_profit = total_amount - today_sales.aggregate(Sum('sell_quantity', field='sell_quantity*product__buying_price'))['sell_quantity__sum']
    context = {'date': today, 'quantities': quantities, 'total_amount': total_amount, 'total_profit': total_profit}
    return render(request, 'daily_report.html', context)


@login_required
def report(request, type):
    values = type.split(',')
    today = datetime.now().date()
    if type == 'daily':
        yesterday = today - timedelta(days=1)
        # Get the quantities sold for each product on the current day
        today_sales = Sell.objects.filter(Q(sell_at=today) | Q(update_at=today))
        today_quantities = today_sales.values('product', 'product__product_name', 'product__brand_name', 'product__buying_price', 'product__product_quantity', 'product__expecting_selling_price').annotate(
            total_quantity=Sum('sell_quantity'),
            total_sale_amount=Sum('total_sell_price'),
            total_profit=Sum((F('total_sell_price') - F('product__remining_quantity')))
        ).order_by('product')

        # Get the total quantities sold for each product, including previous days
        previous_sales = Sell.objects.filter(Q(sell_at=yesterday) | Q(update_at=yesterday)).values('product').annotate(total_quantity=Sum('sell_quantity')).order_by('product')
        
        # Merge the two querysets to get the updated quantities for each product
        quantities = []
        for today_quantity in today_quantities:
            for previous_quantity in previous_sales:
                if today_quantity['product'] == previous_quantity['product']:
                    today_quantity['total_quantity'] += today_quantity['total_quantity']
                    break
            quantities.append(today_quantity)


    elif type == 'weekly':
        week_ago = today - timedelta(days=7)
        # Get the quantities sold for each product on the current day
        today_sales = Sell.objects.filter(Q(sell_at=today) | Q(update_at=today))
        today_quantities = today_sales.values('product', 'product__product_name', 'product__brand_name', 'product__buying_price', 'product__product_quantity', 'product__expecting_selling_price').annotate(
            total_quantity=Sum('sell_quantity'),
            total_sale_amount=Sum('total_sell_price'),
            total_profit=Sum((F('total_sell_price') - F('product__remining_quantity')))
        ).order_by('product')


        # Get the total quantities sold for each product, including previous days
        previous_sales = Sell.objects.filter(Q(sell_at=week_ago) | Q(update_at=week_ago)).values('product').annotate(total_quantity=Sum('sell_quantity')).order_by('product')
        
        # Merge the two querysets to get the updated quantities for each product
        quantities = []
        for today_quantity in today_quantities:
            for previous_quantity in previous_sales:
                if today_quantity['product'] == previous_quantity['product']:
                    today_quantity['total_quantity'] += today_quantity['total_quantity']
                    break
            quantities.append(today_quantity)
    
    elif type == 'monthly':
        month_ago = today - timedelta(days=30)
        today_sales = Sell.objects.filter(Q(sell_at=today) | Q(update_at=today))
        today_quantities = today_sales.values('product', 'product__product_name', 'product__brand_name', 'product__buying_price', 'product__product_quantity', 'product__expecting_selling_price').annotate(
            total_quantity=Sum('sell_quantity'),
            total_sale_amount=Sum('total_sell_price'),
            total_profit=Sum((F('total_sell_price') - F('product__remining_quantity')))
        ).order_by('product')

        # Get the total quantities sold for each product, including previous days
        previous_sales = Sell.objects.filter(Q(sell_at=month_ago) | Q(update_at=month_ago)).values('product').annotate(total_quantity=Sum('sell_quantity')).order_by('product')
        
        # Merge the two querysets to get the updated quantities for each product
        quantities = []
        for today_quantity in today_quantities:
            for previous_quantity in previous_sales:
                if today_quantity['product'] == previous_quantity['product']:
                    today_quantity['total_quantity'] += today_quantity['total_quantity']
                    break
            quantities.append(today_quantity)

    total_amount = today_sales.aggregate(Sum('total_sell_price'))['total_sell_price__sum']
    total_profit = total_amount - today_sales.aggregate(Sum('sell_quantity', field='sell_quantity*product__buying_price'))['sell_quantity__sum']
    
    context = {
        'date': today, 
        'quantities': quantities, 
        'total_amount': total_amount, 
        'total_profit': total_profit,
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




def accessories_summary(request):
    todays_date = datetime.date.today()
    months_ago = todays_date-datetime.timedelta(days=30)
    items = Product.objects.filter(owner=request.user, date__gte=months_ago, date__lte=todays_date)
    finalrep = {}

    def get_product_item(item):
        return item.product_name
    item_list = list(set(map(get_product_item, items)))

    def get_product_quantity(quantity):
        product_quntity = 0
        filtered_by_product_quntity = items.filter(quantity=quantity)

        for p_item in filtered_by_product_quntity:
            product_quntity += p_item.product_quantity

        print(product_quntity)
        return product_quntity
    
        

    for x in items:
        for y in item_list:
            finalrep[y] = get_product_quantity(y)

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





def calculate_profit(request):
    pass
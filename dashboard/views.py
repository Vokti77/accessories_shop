from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accessories.models import Product, Sale, Brand, Model
from account.models import MyUser
from django.contrib.auth.models import User
from dashboard.forms import ModelForm, ProductsForm, SaleForm, BrandForm, SearchForm
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
    total_Sale_amount = 0
    total_profit = 0
    profit = 0

    product_item = Product.objects.all()
    user = MyUser.objects.count()
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
        'user': user,
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
        # brand = request.GET.get('brand')   # Filter by Brand
        # model = request.GET.get('model')   # Filter by Model

        # if model == None:
        #     product_item = Product.objects.all()
        # else:
        #     product_item = Product.objects.filter(model__name=model)
       

        # if brand == None:
        #     models  = Model.objects.all()
        # else:
        #     models = Model.objects.filter(brand__name=brand)

        # if brand == brand and model == model:
        #     queary = Q(Q(brand__name=brand) | Q(model__name=model))
        #     product_item = Product.objects.filter(queary)
        # else:
        #     product_item = Product.objects.all()

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

    
        
            # models = Model.objects.filter(brand__name=brand)
        # elif model == model:
        #     product_item = Product.objects.filter(model__name=model)
        # else:
        #     product_item = Product.objects.all()
        

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
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    # Get the quantities sold for each product on the current day
    today_sales = Sale.objects.filter(Q(sale_at=today) | Q(update_at=today))
    today_quantities = today_sales.values('product', 'product__product_name').annotate(
        total_quantity=Sum('sale_quantity'),
        total_profit=Sum(F('sale_quantity') * (F('sale_price') - F('product__buying_price')))
    ).order_by('product')

    # today_quantities = today_sales.values('product', 'product__product_name', 'product__buying_price').annotate(total_quantity=Sum('sale_quantity')).order_by('product')
   
    # Get the total quantities sold for each product, including previous days
    previous_sales = Sale.objects.filter(Q(sale_at=yesterday) | Q(update_at=yesterday)).values('product').annotate(total_quantity=Sum('sale_quantity')).order_by('product')
    
    # Merge the two querysets to get the updated quantities for each product
    quantities = []
    for today_quantity in today_quantities:
        for previous_quantity in previous_sales:
            if today_quantity['product'] == previous_quantity['product']:
                today_quantity['total_quantity'] += today_quantity['total_quantity']
                break
        quantities.append(today_quantity)

    total_amount = today_sales.aggregate(Sum('sale_price'))['sale_price__sum']
    total_profit = total_amount - today_sales.aggregate(Sum('sale_quantity', field='sale_quantity*product__buying_price'))['sale_quantity__sum']
    context = {'date': today, 'quantities': quantities, 'total_amount': total_amount, 'total_profit': total_profit}
    return render(request, 'daily_report.html', context)


@login_required
def report(request, type):
    values = type.split(',')
    today = datetime.now().date()
    if type == 'daily':
        yesterday = today - timedelta(days=1)
        # Get the quantities sold for each product on the current day
        today_sales = Sale.objects.filter(Q(sale_at=today) | Q(update_at=today))
        today_quantities = today_sales.values('product', 'product__product_name', 'product__model', 'product__buying_price', 'product__product_quantity', 'product__expecting_Saleing_price').annotate(
            total_quantity=Sum('sale_quantity'),
            total_sale_amount=Sum('total_Sale_price'),
            total_profit=Sum((F('total_Sale_price') - F('product__remining_quantity')))
        ).order_by('product')

        # Get the total quantities sold for each product, including previous days
        previous_sales = Sale.objects.filter(Q(sale_at=yesterday) | Q(update_at=yesterday)).values('product').annotate(total_quantity=Sum('sale_quantity')).order_by('product')
        
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
        today_sales = Sale.objects.filter(Q(sale_at=today) | Q(update_at=today))
        today_quantities = today_sales.values('product', 'product__product_name', 'product__model', 'product__buying_price', 'product__product_quantity', 'product__expecting_Saleing_price').annotate(
            total_quantity=Sum('sale_quantity'),
            total_sale_amount=Sum('total_Sale_price'),
            total_profit=Sum((F('total_Sale_price') - F('product__remining_quantity')))
        ).order_by('product')


        # Get the total quantities sold for each product, including previous days
        previous_sales = Sale.objects.filter(Q(sale_at=week_ago) | Q(update_at=week_ago)).values('product').annotate(total_quantity=Sum('sale_quantity')).order_by('product')
        
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
        today_sales = Sale.objects.filter(Q(sale_at=today) | Q(update_at=today))
        today_quantities = today_sales.values('product', 'product__product_name', 'product__model', 'product__buying_price', 'product__product_quantity', 'product__expecting_Saleing_price').annotate(
            total_quantity=Sum('sale_quantity'),
            total_sale_amount=Sum('total_Sale_price'),
            total_profit=Sum((F('total_Sale_price') - F('product__remining_quantity')))
        ).order_by('product')

        # Get the total quantities sold for each product, including previous days
        previous_sales = Sale.objects.filter(Q(sale_at=month_ago) | Q(update_at=month_ago)).values('product').annotate(total_quantity=Sum('sale_quantity')).order_by('product')
        
        # Merge the two querysets to get the updated quantities for each product
        quantities = []
        for today_quantity in today_quantities:
            for previous_quantity in previous_sales:
                if today_quantity['product'] == previous_quantity['product']:
                    today_quantity['total_quantity'] += today_quantity['total_quantity']
                    break
            quantities.append(today_quantity)

    total_amount = today_sales.aggregate(Sum('total_Sale_price'))['total_Sale_price__sum']
   
    
    context = {
        'date': today, 
        'quantities': quantities, 
        'total_amount': total_amount, 
        
        'values': values
        }
    return render(request, 'dashboard/report.html', context)


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

def search_datalist(request):
    q_set = Product.objects.all()
    form = SearchForm(request.POST or None)
    context ={
        'form': form,
        'q_set': q_set
    }
    if request.method == 'POST':
        model = form['model'].value()
        q_set = Product.objects.filter(product_name__icontains=form['product_name'].value())

        if (model != ''):
            q_set = q_set.filter(model_id=model)

    context ={
        'form': form,
        'q_set': q_set
    }
    return render(request, 'search.html', context)

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
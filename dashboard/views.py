from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accessories.models import Product, Sale, Brand, Model, ProductQuantityHistory
from account.models import MyUser
from django.contrib.auth.models import User
from dashboard.forms import ModelForm, ProductsForm, BrandForm, SearchForm
from dashboard.models import * 
from django.db.models import Q, F, Count, F, Sum, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date
from django.http import JsonResponse
import datetime
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


@login_required(login_url='account:login')
def index(request):
    total_amount = 0
    total_item = 0
    total_Sale_amount = 0
    total_profit = 0
    profit = 0

    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    
    sales = len(Sale.objects.all())

    transaction = len(Sale.objects.filter(
        sale_at__year=current_year,
        sale_at__month = current_month,
    
    ))

    today_sales = Sale.objects.filter(
        sale_at__year=current_year,
        sale_at__month = current_month,
        sale_at__day = current_day
    ).all()

    today_sale_amount = sum(today_sales.values_list('total_Sale_price', flat=True))
    today_profit = 0
    for sale in today_sales:
        today_profit += (sale.total_Sale_price - sale.product.buying_price * sale.sale_quantity)
            
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
        'sales': sales,
        'total_item': total_item,
        'total_amount': total_amount,
        'total_profit' : total_profit,
        'total_Sale_amount':total_Sale_amount,
        'profit' : profit,
        'low_quantity_products': low_quantity_products,
        'today_sale_amount': today_sale_amount,
        'today_profit': today_profit
        
    } 
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='account:login')
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
        product_item = Product.objects.all().order_by('added_at')
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

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(product_item, 4)
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
        'paginator': paginator,
        'low_quantity_products': low_quantity_products
    }
    return render(request, ['dashboard/tables.html', 'dashboard/index.html'], context)

@login_required(login_url='account:login')
def add_product(request):
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

@login_required(login_url='account:login')
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

@login_required(login_url='account:login')
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

@login_required(login_url='account:login')
def update_product_quantity(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product_id': product_id,
        'product' : product
    }
    return render(request, 'product/update_quantity.html', context)

@login_required(login_url='account:login')
def confirm_update_quantity(request, product_id):
    quantity = int(request.POST.get('quantity'))
    buy_price = int(request.POST.get('buy'))

    add_q = Product.objects.get(id=product_id)
    add_info = ProductQuantityHistory(product=add_q, quantity_added=quantity, buying_price=buy_price)
    add_info.save()

    add_q.product_quantity += quantity
    add_q.buying_price = buy_price
    add_q.save()
    return redirect('dashboard:tables')

@login_required(login_url='account:login')
def update_quntity_history(request):
    total_amount = 0

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('current_year', current_year)

        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        history = ProductQuantityHistory.objects.all().order_by('added_at')

        if month and len(month) == 2:
            history = history.filter(added_at__month=month, added_at__year=year)

        elif from_date and to_date:
            history = history.filter(added_at__range=[from_date, to_date])

        total_amount = sum(history.values_list('buying_price', flat=True))

        return render(request, 'product/history.html', {'history': history, 'total_amount': total_amount})

    else:
        history = ProductQuantityHistory.objects.all().order_by('added_at')
        total = sum(history.values_list('buying_price', flat=True))
        total_amount = sum(history.values_list('buying_price', flat=True))
        return render(request, 'product/history.html', {'history': history, 'total': total, 'total_amount': total_amount})
 
 
@login_required(login_url='account:login')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, "The product has been delete successfully!")
    return redirect('tables')

@login_required(login_url='account:login')
def sale_quantity(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product_id': product_id,
        'product' : product
    }
    return render(request, 'product/sell.html', context)

@login_required(login_url='account:login')
def confirm_Sale(request, product_id):
    try:
        quantity = int(request.POST.get('quantity'))
        sale_price = int(request.POST.get('price'))
        sale = Sale.objects.filter(product_id=product_id).first()
        sale_q = Product.objects.get(id=product_id)
        
        # if sale:
        #     sale.sale_quantity += quantity
        #     sale.sale_price += sale_price
        #     sale.total_Sale_price += (sale_price*quantity)
        #     sale.save()
        # else:
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
        return redirect('dashboard:tables')
        raise Exception("Something wrong")

from datetime import datetime
@login_required(login_url='account:login')
def report(request):
    total_amount = 0
    total_profit = 0

    # get the current year and month
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('current_year', current_year)

        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        queryset = Sale.objects.all().order_by('sale_at')

        if month and len(month) == 2:
            queryset = queryset.filter(sale_at__month=month, sale_at__year=year)
        elif from_date and to_date:
            queryset = queryset.filter(sale_at__range=[from_date, to_date])

        total_amount = sum(queryset.values_list('total_Sale_price', flat=True))
        for sale in queryset:
            total_profit +=  sale.profit           # (sale.total_Sale_price - sale.product.buying_price * sale.sale_quantity)

        return render(request, 'dashboard/report.html', {'queryset': queryset, 'total_amount': total_amount, 'total_profit': total_profit})

    else:
        queryset = Sale.objects.all().order_by('sale_at')
        total = sum(queryset.values_list('sale_quantity', flat=True))
        total_amount = sum(queryset.values_list('total_Sale_price', flat=True))

        for sale in queryset:
            total_profit += sale.profit            #(sale.total_Sale_price - sale.product.buying_price * sale.sale_quantity)

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
    grouped_purchases = purchases.annotate(price=F("profit")).annotate(month=ExtractMonth("sale_at"))\
        .values("month").annotate(average=Avg("profit")).values("month", "average").order_by("month")

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

def statistics_view(request):
    return render(request, "statistics.html", {})










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


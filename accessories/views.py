from django.shortcuts import render, redirect, reverse

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, ListView
from django_pandas.io import read_frame
import plotly
import plotly.express as ex
import json
import csv

from .models import Product, Sell
from .forms import ProductForm
from .model_choices import *

def home(request):
    return render(request, 'accounts/login.html')

def index(request):
    product_item = Product.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(product_item, 2)

    try:
        product_item = paginator.page(page)

    except PageNotAnInteger:
        # fall back to first page
        product_item = paginator.page(1)
    except EmptyPage:
        # fall back to last page
        product_item = paginator.page(paginator.num_pages)

    context = {
         'product_item' : product_item,
     }
    return render(request, 'dashboard/tables.html', context)   


def add_(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, "product/home.html", context)


def edit_(request, p_id):
    product = Product.objects.get(id=p_id)
    form = ProductForm(instance=product)
    context = {
        "form": form,
    }
    product_inc = Product.objects.get(id=p_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product_inc)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'product/home.html', context)


def delete_(request, p_id):
    product = Product.objects.get(id=p_id)
    product.delete()
    return redirect('/')

def sell(request, product_id):
    context = {
        'product_id': product_id,
    }
    return render(request, 'product/sell.html', context)


def confirm_sell(request, product_id):
    quantity = int(request.POST.get('quantity'))
    sell_q = Product.objects.get(id=product_id)
    if sell_q.product_quantity >=quantity:
        sell_q.product_quantity -= quantity
        sell_q.remining_quantity += quantity
        sell_q.save()
        return redirect(reverse('index'))
    else:
        raise Exception("Something wrong") 

def dashbord(request):
    products = Product.objects.all()

    df = read_frame(products)

    quantity_update_graph = df.groupby(by='quantity_update_date', as_index=False, sort=False)['product_quantity'].sum()
    quantity_update_graph = ex.line(quantity_update_graph, x=quantity_update_graph.quantity_update_date, y=quantity_update_graph.product_quantity, title="Update Quantity")
    quantity_update_graph = json.dump(quantity_update_graph, cls=plotly.PlotlyJESONEncoder)

    context = {
        'quantity_update_graph': quantity_update_graph,
    }

    return render(request, 'product/dashbord.html', context)

def search(request):
    product_item = Product.objects.all()
    method_dict = request.GET.copy()
    keywords = method_dict.get('keywords') or None
    brand_name = method_dict.get('brand_name') or None

    page = request.GET.get('page', 1)
    paginator = Paginator(product_item, 2)

    if keywords is not None:
        keyword = method_dict['keywords']
        # product_item = product_item.filter(desc__iexact=keyword)  # django == DJANGO
        product_items = product_item.filter(product_name__icontains=keyword)  # django == Django Web development
       
    if brand_name is not None:
        brand_names = method_dict['brand_name']
        product_item = product_item.filter(brand_name__iexact=brand_names)


    try:
        product_item = paginator.page(page)

    except PageNotAnInteger:
        # fall back to first page
        product_item = paginator.page(1)
    except EmptyPage:
        # fall back to last page
        product_item = paginator.page(paginator.num_pages)

    context = {
        'method_dict': method_dict,
        'product_items': product_items,
       
    }

    return render(request, 'product/search.html', context)



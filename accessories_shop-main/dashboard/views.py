from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, F, Q, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from account.models import MyUser
from accessories.models import Brand, Model, Product, ProductQuantityHistory, Sale
from dashboard.forms import BrandForm, ModelForm, ProductsForm, SearchForm
from service.models import Service
from utils.charts import colorPrimary, get_year_dict, months


def _decimal_from_post(request, key):
    try:
        return Decimal(request.POST.get(key, "0"))
    except (InvalidOperation, TypeError):
        raise ValueError(f"Invalid value for {key}.")


def _product_queryset():
    return Product.objects.select_related("brand", "model")


def _show_low_stock_messages(request, products):
    for product in products:
        if product.product_quantity < 5:
            messages.warning(
                request, f"The quantity of {product.product_name} is less than 5!"
            )


@login_required(login_url="account:login")
def index(request):
    today = timezone.localdate()
    products = list(_product_queryset())
    today_sales = Sale.objects.select_related("product").filter(sale_at=today)

    aggregates = Product.objects.aggregate(
        total_stock_value=Sum(F("buying_price") * F("product_quantity")),
        total_sale_amount=Sum("actual_Sale_price"),
    )
    sales_aggregates = today_sales.aggregate(
        today_sale_amount=Sum("total_Sale_price"),
        today_profit=Sum("profit"),
    )

    _show_low_stock_messages(request, products)

    context = {
        "users": MyUser.objects.count(),
        "model_item": Model.objects.all(),
        "product_item": products,
        "sales": Sale.objects.count(),
        "total_item": len(products),
        "total_amount": aggregates["total_stock_value"] or 0,
        "total_profit": sum(product.current_profit for product in products),
        "total_Sale_amount": aggregates["total_sale_amount"] or 0,
        "profit": 0,
        "low_quantity_products": Product.objects.filter(product_quantity__lt=5).count(),
        "today_sale_amount": sales_aggregates["today_sale_amount"] or 0,
        "today_profit": sales_aggregates["today_profit"] or 0,
        "today_servicing_amount": Service.objects.filter(date_added=today).aggregate(
            total=Sum("sevicing_cost")
        )["total"]
        or 0,
    }
    return render(request, "dashboard/index.html", context)


@login_required(login_url="account:login")
def tables(request):
    form = SearchForm(request.POST or None)
    product_item = _product_queryset()

    query = request.GET.get("quary_set")
    brand_id = request.GET.get("brands")

    if query:
        product_item = product_item.filter(
            Q(product_name__icontains=query)
            | Q(model__name__icontains=query)
            | Q(brand__name__icontains=query)
        )
    elif request.method == "POST" and form.is_valid() and form.cleaned_data.get("model"):
        product_item = product_item.filter(model=form.cleaned_data["model"])
    elif brand_id:
        product_item = product_item.filter(brand_id=brand_id)

    products = list(product_item)
    _show_low_stock_messages(request, products)

    context = {
        "form": form,
        "product_item": products,
        "total_item": len(products),
        "brands": Brand.objects.all(),
        "models": Model.objects.select_related("brand"),
        "total_amount": sum(p.buying_price * p.product_quantity for p in products),
        "profit": 0,
        "total_profit": sum(p.current_profit for p in products),
        "total_Sale_amount": sum(p.actual_Sale_price for p in products),
        "low_quantity_products": Product.objects.filter(product_quantity__lt=5).count(),
    }
    return render(request, "dashboard/tables.html", context)


@login_required(login_url="account:login")
def add_product(request):
    form = ProductsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "The product has been added successfully!")
        return redirect("dashboard:add-product")
    return render(request, "dashboard/form_product.html", {"form": form})


@login_required(login_url="account:login")
def get_models(request):
    brand_id = request.GET.get("brand_id")
    models = Model.objects.filter(brand_id=brand_id).values("id", "name")
    return JsonResponse(list(models), safe=False)


@login_required(login_url="account:login")
def add_brand(request):
    form = BrandForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "The brand has been added successfully!")
        return redirect("dashboard:add-brand")
    return render(
        request,
        "dashboard/form_brand.html",
        {"form": form, "brands": Brand.objects.all()},
    )


@login_required(login_url="account:login")
def add_model(request):
    form = ModelForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "The model has been added successfully!")
        return redirect("dashboard:add-model")
    context = {
        "form": form,
        "models": Model.objects.select_related("brand"),
        "brands": Brand.objects.all(),
    }
    return render(request, "dashboard/form_model.html", context)


@login_required(login_url="account:login")
def upadate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductsForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:tables")
    return render(request, "product/update.html", {"form": form})


@login_required(login_url="account:login")
def upadate_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    form = BrandForm(request.POST or None, instance=brand)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:add-brand")
    return render(request, "product/brand_update.html", {"form": form})


@login_required(login_url="account:login")
def upadate_model(request, model_id):
    model = get_object_or_404(Model, id=model_id)
    form = ModelForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard:add-model")
    return render(request, "product/update_model.html", {"form": form})


@login_required(login_url="account:login")
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    brand.delete()
    messages.success(request, "The brand has been deleted successfully!")
    return redirect("dashboard:add-brand")


@login_required(login_url="account:login")
def update_product_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        "product/update_quantity.html",
        {"product_id": product_id, "product": product},
    )


@login_required(login_url="account:login")
@require_POST
def confirm_update_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 0))
        buy_price = _decimal_from_post(request, "buy")
        sell_price = _decimal_from_post(request, "sell")
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))

    if quantity <= 0:
        return HttpResponseBadRequest("Quantity must be greater than zero.")

    with transaction.atomic():
        ProductQuantityHistory.objects.create(
            product=product,
            quantity_added=quantity,
            buying_price=buy_price,
            new_selling_price=sell_price,
        )
        product.product_quantity = F("product_quantity") + quantity
        product.buying_price = buy_price
        product.expecting_Saleing_price = sell_price
        product.save(
            update_fields=["product_quantity", "buying_price", "expecting_Saleing_price"]
        )

    return redirect("dashboard:tables")


@login_required(login_url="account:login")
def update_quntity_history(request):
    history = ProductQuantityHistory.objects.select_related("product").all()
    current_year = timezone.localdate().year

    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("current_year") or current_year
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        if month and len(month) == 2:
            history = history.filter(added_at__month=month, added_at__year=year)
        elif from_date and to_date:
            history = history.filter(added_at__range=[from_date, to_date])

    total_amount = history.aggregate(total=Sum("buying_price"))["total"] or 0
    return render(
        request,
        "product/history.html",
        {"history": history, "total": total_amount, "total_amount": total_amount},
    )


@login_required(login_url="account:login")
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "The product has been deleted successfully!")
    return redirect("dashboard:tables")


@login_required(login_url="account:login")
def sale_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        "product/sell.html",
        {
            "product_id": product_id,
            "product": product,
            "stock_quantity": product.product_quantity,
        },
    )


@login_required(login_url="account:login")
@require_POST
def confirm_Sale(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 0))
        sale_price = _decimal_from_post(request, "price")
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))

    if quantity <= 0:
        return HttpResponseBadRequest("Quantity must be greater than zero.")
    if product.product_quantity < quantity:
        messages.error(request, "Not enough stock available for this sale.")
        return redirect("dashboard:Sale-quantity", product_id=product_id)

    with transaction.atomic():
        sale = Sale.objects.create(
            sale_quantity=quantity,
            sale_price=sale_price,
            product=product,
            sale_at=timezone.localdate(),
        )
        product.product_quantity = F("product_quantity") - quantity
        product.sale_quantity = F("sale_quantity") + quantity
        product.remining_quantity = F("remining_quantity") + (product.buying_price * quantity)
        product.actual_Sale_price = F("actual_Sale_price") + sale.total_Sale_price
        product.save(
            update_fields=[
                "product_quantity",
                "sale_quantity",
                "remining_quantity",
                "actual_Sale_price",
            ]
        )

    return redirect("dashboard:tables")


@login_required(login_url="account:login")
def report(request):
    queryset = Sale.objects.select_related("product").all()
    current_year = timezone.localdate().year

    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("current_year") or current_year
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        if month and len(month) == 2:
            queryset = queryset.filter(sale_at__month=month, sale_at__year=year)
        elif from_date and to_date:
            queryset = queryset.filter(sale_at__range=[from_date, to_date])

    aggregates = queryset.aggregate(
        total=Sum("sale_quantity"),
        total_amount=Sum("total_Sale_price"),
        total_profit=Sum("profit"),
    )
    context = {
        "queryset": queryset,
        "total": aggregates["total"] or 0,
        "total_amount": aggregates["total_amount"] or 0,
        "total_profit": aggregates["total_profit"] or 0,
    }
    return render(request, "dashboard/report.html", context)


@login_required(login_url="account:login")
def get_filter_options(request):
    grouped_purchases = (
        Sale.objects.annotate(year=ExtractYear("sale_at"))
        .values("year")
        .order_by("-year")
        .distinct()
    )
    return JsonResponse({"options": [purchase["year"] for purchase in grouped_purchases]})


@login_required(login_url="account:login")
def get_sales_chart(request, year):
    grouped_purchases = (
        Sale.objects.filter(sale_at__year=year)
        .annotate(month=ExtractMonth("sale_at"))
        .values("month")
        .annotate(average=Avg("total_Sale_price"))
        .order_by("month")
    )
    data = get_year_dict()
    for group in grouped_purchases:
        data[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse(
        {
            "title": f"Spend per customer in {year}",
            "data": {
                "labels": list(data.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": colorPrimary,
                        "borderColor": colorPrimary,
                        "data": list(data.values()),
                    }
                ],
            },
        }
    )


@login_required(login_url="account:login")
def spend_per_customer_chart(request, year):
    grouped_purchases = (
        Sale.objects.filter(sale_at__year=year)
        .annotate(month=ExtractMonth("sale_at"))
        .values("month")
        .annotate(average=Avg("profit"))
        .order_by("month")
    )
    data = get_year_dict()
    for group in grouped_purchases:
        data[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse(
        {
            "title": f"Profit per customer in {year}",
            "data": {
                "labels": list(data.keys()),
                "datasets": [
                    {
                        "label": "Amount ($)",
                        "backgroundColor": colorPrimary,
                        "borderColor": colorPrimary,
                        "data": list(data.values()),
                    }
                ],
            },
        }
    )


@login_required(login_url="account:login")
def statistics_view(request):
    return render(request, "statistics.html", {})


@login_required(login_url="account:login")
def charts(request):
    return render(request, "dashboard/charts.html")


@login_required(login_url="account:login")
def widgets(request):
    return render(request, "dashboard/widgets.html")


@login_required(login_url="account:login")
def grid(request):
    return render(request, "dashboard/grid.html")


@login_required(login_url="account:login")
def form_basic(request):
    return render(request, "dashboard/form_basic.html")


@login_required(login_url="account:login")
def form_wizard(request):
    return render(request, "dashboard/form_wizard.html")


@login_required(login_url="account:login")
def buttons(request):
    return render(request, "dashboard/buttons.html")


@login_required(login_url="account:login")
def icon_material(request):
    return render(request, "dashboard/icon-material.html")


@login_required(login_url="account:login")
def icon_fontawesome(request):
    return render(request, "dashboard/icon-fontawesome.html")


@login_required(login_url="account:login")
def elements(request):
    return render(request, "dashboard/elements.html")


@login_required(login_url="account:login")
def gallery(request):
    return render(request, "dashboard/gallery.html")


@login_required(login_url="account:login")
def invoice(request):
    return render(request, "dashboard/invoice.html")

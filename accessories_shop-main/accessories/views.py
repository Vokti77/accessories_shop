import calendar
from django.db.models import Sum, F
from datetime import datetime
from django.utils import timezone
from calendar import month_name
from django.shortcuts import render
from django.db.models.functions import ExtractMonth
from accessories.models import Product, Sale, MonthlySaleProfitHistory

def calculate_monthly_sale_profit():
    # Get the current month and year
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year


    # current month
    start_date = datetime(current_year, current_month, 1)
    end_date = datetime(current_year, current_month, 1).replace(day=1, month=current_month % 12 + 1)

    # Check current month
    monthly_data = MonthlySaleProfitHistory.objects.filter(date_added__range=[start_date, end_date]).first()

    if monthly_data:
      
        stock_data = Product.objects.filter(added_at__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('product_quantity'),
            total_amount=Sum('product_quantity') * F('buying_price')
        )
        stock_quantity = stock_data['total_quantity']
        stock_amount = stock_data['total_amount']

        sale_data = Sale.objects.filter(sale_at__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('sale_quantity'),
            total_amount=Sum('total_Sale_price'),
            total_profit=Sum('profit')
        )
        sale_quantity = sale_data['total_quantity']
        sale_amount = sale_data['total_amount']
        profit = sale_data['total_profit']

        monthly_data.stock_quantity = stock_quantity
        monthly_data.stock_amount = stock_amount
        monthly_data.sale_quantity = sale_quantity
        monthly_data.sale_amount = sale_amount
        monthly_data.profit = profit
        monthly_data.save()
    else:
    
        stock_data = Product.objects.filter(added_at__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('product_quantity'),
            total_amount=Sum('product_quantity') * F('buying_price')
        )
        stock_quantity = stock_data['total_quantity']
        stock_amount = stock_data['total_amount']

      
        sale_data = Sale.objects.filter(sale_at__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('sale_quantity'),
            total_amount=Sum('total_Sale_price'),
            total_profit=Sum('profit')
        )
        sale_quantity = sale_data['total_quantity']
        sale_amount = sale_data['total_amount']
        profit = sale_data['total_profit']

        monthly_data = MonthlySaleProfitHistory.objects.create(
            stock_quantity=stock_quantity,
            stock_amount=stock_amount,
            sale_quantity=sale_quantity,
            sale_amount=sale_amount,
            profit=profit,
            date_added=current_date
        )



def monthly_sale_profit_view(request):

    current_date = datetime.now()
    current_month = current_date.month


    monthly_data = MonthlySaleProfitHistory.objects.annotate(month=ExtractMonth('date_added')).values(
        'month', 'stock_quantity', 'stock_amount', 'sale_quantity', 'sale_amount', 'profit'
    ).order_by('month')

    data_by_month = {}
    for data in monthly_data:
        month_number = data['month']
        month = calendar.month_name[month_number]
        data_by_month[month] = {
            'stock_quantity': data['stock_quantity'],
            'stock_amount': data['stock_amount'],
            'sale_quantity': data['sale_quantity'],
            'sale_amount': data['sale_amount'],
            'profit': data['profit']
        }

    context = {
        'data_by_month': data_by_month,
        'current_month': calendar.month_name[current_month]
    }

    return render(request, 'monthly_sale_profit.html', context)


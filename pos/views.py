import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from products.models import Product, Category
from sales.models import Sale
from django.utils.timezone import localdate
from django.utils.timezone import localdate, timedelta ,now

@login_required(login_url="/accounts/login/")
def index(request):
    today = now().date()
    yesterday = today - timedelta(days=1)

    # Calculate total sales for today
    total_sales_today = (
        Sale.objects.filter(date_added__date=today)
        .aggregate(total=Sum('grand_total'))
        .get('total', 0) or 0
    )

    # Calculate total sales for yesterday
    total_sales_yesterday = (
        Sale.objects.filter(date_added__date=yesterday)
        .aggregate(total=Sum('grand_total'))
        .get('total', 0) or 0
    )

    # Calculate the percentage change
    if total_sales_yesterday > 0:
        percentage_change = ((total_sales_today - total_sales_yesterday) / total_sales_yesterday) * 100
    else:
        percentage_change = 100 if total_sales_today > 0 else 0

    # Determine if the change is an increase or decrease
    if percentage_change > 0:
        change_type = "increase"
    elif percentage_change < 0:
        change_type = "decrease"
    else:
        change_type = "no change"

    # Format the percentage change
    formatted_percentage_change = f"{abs(percentage_change):.2f}% {change_type}"

    today = date.today()

    year = today.year
    monthly_earnings = []

    # Calculate earnings per month
    for month in range(1, 13):
        earning = Sale.objects.filter(date_added__year=year, date_added__month=month).aggregate(
            total_variable=Coalesce(Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
        monthly_earnings.append(earning)

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(date_added__year=year).aggregate(total_variable=Coalesce(
        Sum(F('grand_total')), 0.0, output_field=FloatField())).get('total_variable')
    annual_earnings = format(annual_earnings, '.2f')

    # AVG per month
    avg_month = format(sum(monthly_earnings)/12, '.2f')

    # Top-selling products
    top_products = Product.objects.annotate(quantity_sum=Sum(
        'saledetail__quantity')).order_by('-quantity_sum')[:3]
    # Get today's sales
    today_sales = Sale.objects.filter(date_added__date=localdate())
    # Calculate total sales for today
    total_sales_today = Sale.objects.filter(date_added__date=localdate()).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    top_products_names = []
    top_products_quantity = []

    for p in top_products:
        top_products_names.append(p.name)
        top_products_quantity.append(p.quantity_sum)

    print(top_products_names)
    print(top_products_quantity)
     

    latest_orders = Sale.objects.order_by('-date_added')[:5]
    context = {
        'sales': today_sales,
        'total_sales': total_sales_today,
        'latest_orders': latest_orders,
        "active_icon": "dashboard",
        "products": Product.objects.all().count(),
        "categories": Category.objects.all().count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_names_list": top_products_names,
        "top_products_quantity": json.dumps(top_products_quantity),

        'total_sales_today': total_sales_today,
        'total_sales_yesterday': total_sales_yesterday,
        'percentage_change': formatted_percentage_change,
    }
    return render(request, "pos/index.html", context)



def help_and_support(request):
    return render(request, "pos/help_and_support.html")
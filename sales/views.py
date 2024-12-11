import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from customers.models import Customer
from products.models import Product
from xhtml2pdf import pisa  # Replace WeasyPrint with xhtml2pdf
from .models import Sale, SaleDetail
import json
from io import BytesIO
from django.db.models import Sum, Count



# Your other functions remain the same...
# is_ajax, sales_list_view, sales_add_view, sales_details_view

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def sales_list_view(request):
    context = {
        "active_icon": "sales",
        "sales": Sale.objects.all().order_by('-date_added')  # Order by recent sales
    }
    return render(request, "sales/sales.html", context=context)


@login_required(login_url="/accounts/login/")
def sales_add_view(request):
    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()]
    }

    if request.method == 'POST':
        if is_ajax(request=request):
            # Save the POST arguments
            data = json.load(request)

            sale_attributes = {
                "customer": Customer.objects.get(id=int(data['customer'])),
                "sub_total": float(data["sub_total"]),
                "grand_total": float(data["grand_total"]),
                "tax_amount": float(data["tax_amount"]),
                "tax_percentage": float(data["tax_percentage"]),
                "amount_payed": float(data["amount_payed"]),
                "amount_change": float(data["amount_change"]),
            }
            try:
                # Create the sale
                new_sale = Sale.objects.create(**sale_attributes)
                new_sale.save()
                # Create the sale details
                products = data["products"]

                for product in products:
                    detail_attributes = {
                        "sale": Sale.objects.get(id=new_sale.id),
                        "product": Product.objects.get(id=int(product["id"])),
                        "price": product["price"],
                        "quantity": product["quantity"],
                        "total_detail": product["total_product"]
                    }
                    sale_detail_new = SaleDetail.objects.create(
                        **detail_attributes)
                    sale_detail_new.save()

                print("Sale saved")

                messages.success(
                    request, 'Sale created successfully!', extra_tags="success")

            except Exception as e:
                messages.success(
                    request, 'There was an error during the creation!', extra_tags="danger")

        return redirect('sales:sales_list')

    return render(request, "sales/sales_add.html", context=context)


@login_required(login_url="/accounts/login/")
def sales_details_view(request, sale_id):
    """
    Args:
        request:
        sale_id: ID of the sale to view
    """
    try:
        # Get the sale
        sale = Sale.objects.get(id=sale_id)

        # Get the sale details
        details = SaleDetail.objects.filter(sale=sale)

        context = {
            "active_icon": "sales",
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.success(
            request, 'There was an error getting the sale!', extra_tags="danger")
        print(e)
        return redirect('sales:sales_list')



def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


@login_required(login_url="/accounts/login/")
def receipt_pdf_view(request, sale_id):
    """
    Args:
        request:
        sale_id: ID of the sale to view the receipt
    """
    try:
        # Get the sale
        sale = Sale.objects.get(id=sale_id)

        # Get the sale details
        details = SaleDetail.objects.filter(sale=sale)

        template = get_template("sales/sales_receipt_pdf.html")
        context = {
            "sale": sale,
            "details": details
        }
        html = template.render(context)
        
        # Create a file-like buffer to receive PDF data
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{sale_id}.pdf"'
        
        # Create PDF
        pisa_status = pisa.CreatePDF(
            html,                   # the HTML to convert
            dest=response,          # the file handle to receive result
            encoding='utf-8',
            link_callback=link_callback,
        )

        # Return response
        if pisa_status.err:
            return HttpResponse('We had some errors creating the PDF <pre>' + html + '</pre>')
        return response

    except Exception as e:
        messages.error(request, f'Error generating PDF: {str(e)}', extra_tags="danger")
        return redirect('sales:sales_list')
    

def search_order(request):
    query = request.GET.get('order_id', '').strip()  # Get the query from the GET parameter
    result = None
    error = None

    if query:  # Only search if there's input
        try:
            result = Sale.objects.get(order_id=query)
        except Sale.DoesNotExist:
            error = "No order found with the provided Order ID."

    return render(request, 'sales/search_order.html', {
        'query': query,
        'result': result,
        'error': error,
    })


#sales report 
from django.shortcuts import render
from django.db.models import Sum
from .models import Sale, SaleDetail

def sales_report(request):
    # Get all sales
    sales = Sale.objects.all()

    # Total Sales Value (sum of grand_total)
    total_sales_value = sales.aggregate(total_sales=Sum('grand_total'))['total_sales'] or 0

    # Number of Transactions
    number_of_transactions = sales.count()

    # Top-Selling Products (aggregate quantity from SaleDetail)
    top_selling_products = SaleDetail.objects.values('product__name')\
        .annotate(total_sold=Sum('quantity'))\
        .order_by('-total_sold')[:5]

    # Query to get the top 8 most sold items along with their sold quantities and revenue
    sales_data = SaleDetail.objects.values('product__name')\
        .annotate(
            total_quantity_sold=Sum('quantity'),  # Sum of quantity sold
            total_revenue=Sum('quantity') * Sum('price')  # Calculate total revenue
        )\
        .order_by('-total_quantity_sold')[:8]  # Order by quantity sold
    
    # Round the total revenue to 2 decimal places
    for data in sales_data:
        data['total_revenue'] = round(data['total_revenue'], 2)

    # Prepare data for the graph
    products = [data['product__name'] for data in sales_data]
    quantities = [data['total_quantity_sold'] for data in sales_data]  # Quantities sold
    revenues = [data['total_revenue'] for data in sales_data]  # Revenue


    # Query to get the customers who have bought the most items
    customers_data = SaleDetail.objects.values('sale__customer__first_name', 'sale__customer__last_name')\
        .annotate(total_items_bought=Sum('quantity'))\
        .order_by('-total_items_bought')[:5]  # Top 5 customers who bought the most items

    # Query to get the customers who have bought the most items
    customers_data = SaleDetail.objects.values('sale__customer__first_name', 'sale__customer__last_name')\
        .annotate(total_items_bought=Sum('quantity'))\
        .order_by('-total_items_bought')[:5]  # Top 5 customers who bought the most items

    # Prepare data for the table in the template
    customers_info = [
        (f"{data['sale__customer__first_name']} {data['sale__customer__last_name']}", data['total_items_bought'])
        for data in customers_data
    ]

    # Pass the calculated data to the template
    context = {
        'total_sales_value': total_sales_value,
        'number_of_transactions': number_of_transactions,
        'top_selling_products': top_selling_products,
        'products': products,
        'quantities': quantities,
        'revenues': revenues,
        'customers_info': customers_info,
    }

    return render(request, 'reports/sales_report.html', context)


from django.shortcuts import render
from django.db.models import Sum
from .models import Product, SaleDetail

def inventory_report(request):
    # Get all products
    products = Product.objects.all()

    # Initialize a list to store the data we want to display
    inventory_data = []

    # Threshold for low stock (you can adjust this value based on your requirements)
    low_stock_threshold = 10

    # Loop through each product and calculate the stock details
    for product in products:
        # Get total sales quantity for this product
        total_sales = SaleDetail.objects.filter(product=product).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
        
        # Assume the current stock is a value that is either fetched from a field or calculated externally
        # For simplicity, let's say you have a manually set stock quantity in the Product model
        current_stock = product.initial_stock - total_sales  # Assume initial_stock is available in Product

        # Calculate the inventory valuation (current stock * price)
        inventory_valuation = current_stock * product.price

        # Check for low stock warning
        low_stock_warning = current_stock <= low_stock_threshold

        # Append the result for this product
        inventory_data.append({
            'product_name': product.name,
            'category': product.category.name,  # Include the category of the product
            'price': product.price,  # Include the price of the product
            'total_sales': total_sales,
            'current_stock': current_stock,
            'inventory_valuation': inventory_valuation,
            'low_stock_warning': low_stock_warning
        })

    # Pass the data to the template
    context = {
        'inventory_data': inventory_data,
        'low_stock_threshold': low_stock_threshold,
    }

    return render(request, 'reports/inventory_report.html', context)

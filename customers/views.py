from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Customer
from django.shortcuts import get_object_or_404


@login_required(login_url="/accounts/login/")
def customers_list_view(request):
    context = {
        "active_icon": "customers",
        "customers": Customer.objects.all()
    }
    return render(request, "customers/customers.html", context=context)


@login_required(login_url="/accounts/login/")
def customers_add_view(request):
    context = {
        "active_icon": "customers",
    }

    if request.method == 'POST':
        # Save the POST arguments
        data = request.POST

        attributes = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "address": data['address'],
            "email": data['email'],
            "phone": data['phone'],
        }

        # Check if a customer with the same attributes exists
        if Customer.objects.filter(**attributes).exists():
            messages.error(request, 'Customer already exists!',
                           extra_tags="warning")
            return redirect('customers:customers_add')

        try:
            # Create the customer
            new_customer = Customer.objects.create(**attributes)

            # If it doesn't exist save it
            new_customer.save()

            messages.success(request, 'Customer: ' + attributes["first_name"] + " " +
                             attributes["last_name"] + ' created successfully!', extra_tags="success")
            return redirect('customers:customers_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('customers:customers_add')

    return render(request, "customers/customers_add.html", context=context)

@login_required(login_url="/accounts/login/")
def customers_update_view(request, customer_id):
    # Get the customer object or show 404 if not found
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        try:
            # Get form data
            data = request.POST

            # Check if a different customer with the same attributes exists
            if Customer.objects.filter(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            ).exclude(id=customer.id).exists():
                messages.warning(request, 'A customer with similar details already exists.')
                return redirect('customers:customers_update', customer_id=customer_id)

            # Update the customer's details
            customer.first_name = data['first_name']
            customer.last_name = data['last_name']
            customer.address = data['address']
            customer.email = data['email']
            customer.phone = data['phone']
            customer.save()

            # Success message
            messages.success(
                request, f'Customer "{customer.get_full_name()}" updated successfully!'
            )
            return redirect('customers:customers_list')
        except Exception as e:
            messages.error(request, 'An error occurred while updating the customer.')
            print(e)
            return redirect('customers:customers_update', customer_id=customer_id)

    # Render the update form
    context = {
        "active_icon": "customers",
        "customer": customer,
    }
    return render(request, "customers/customers_update.html", context=context)

@login_required(login_url="/accounts/login/")
def customers_delete_view(request, customer_id):
    """
    Args:
        request:
        customer_id : The customer's ID that will be deleted
    """
    try:
        # Get the customer to delete
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(request, '¡Customer: ' + customer.get_full_name() +
                         ' deleted!', extra_tags="success")
        return redirect('customers:customers_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('customers:customers_list')


def search_customer(request):
    query = request.GET.get("customer_name")  # Get the search input
    results = None
    error = None

    if query:
        results = Customer.objects.filter(
            first_name__icontains=query
        ) | Customer.objects.filter(last_name__icontains=query)
        if not results.exists():
            error = f"No customers found matching '{query}'."

    context = {
        "query": query,
        "results": results,
        "error": error,
    }
    return render(request, "customers/search_customer.html", context)
from django.urls import path

from . import views

app_name = "sales"
urlpatterns = [
    # List sales
    path('', views.sales_list_view, name='sales_list'),
    # Add sale
    path('add', views.sales_add_view, name='sales_add'),
    # Details sale
    path('details/<str:sale_id>',
         views.sales_details_view, name='sales_details'),
    # Sale receipt PDF
    path("pdf/<str:sale_id>",
         views.receipt_pdf_view, name="sales_receipt_pdf"),
    path('search-order/', views.search_order, name='search_order'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('sales/inventory-report/', views.inventory_report, name='inventory_report'),  # URL for the inventory report
    path('sales/<int:sale_id>/update/', views.sale_update_view, name='sale_update'),
    path('sales/<int:sale_id>/delete/', views.sale_delete_view, name='sale_delete'),
    path('latest-orders/', views.latest_orders_view, name='latest_orders'),
   
]

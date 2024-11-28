
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication: Login and Logout
    path('', include('authentication.urls')),
    # Index
    path('', include('pos.urls')),
    # Products
    path('products/', include('products.urls')),
    # Customers
    path('customers/', include('customers.urls')),
    # Sales
    path('sales/', include('sales.urls')),
]

# This will allow serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
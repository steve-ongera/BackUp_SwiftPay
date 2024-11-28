from django.db import models
import django.utils.timezone
from django.utils import timezone
from customers.models import Customer
from products.models import Product
import os
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils.timezone import now
from django.conf import settings


class Sale(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey('customers.Customer', on_delete=models.DO_NOTHING, db_column='customer')
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    amount_payed = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    class Meta:
        db_table = 'Sales'

    def __str__(self) -> str:
        return f"Sale ID: {self.id} | Grand Total: {self.grand_total} | Datetime: {self.date_added}"

    def sum_items(self):
        details = SaleDetail.objects.filter(sale=self.id)
        return sum([d.quantity for d in details])

    def save(self, *args, **kwargs):
        # Check if the object already has an ID (i.e., if it's saved in the database)
        if not self.pk:
            # Save the object to generate an ID
            super().save(*args, **kwargs)
        
        # Generate QR code content
        qr_data = f"Sale ID: {self.id}\nCustomer: {self.customer}\nTotal: {self.grand_total}\nDate: {self.date_added}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Save QR code as an image
        img = qr.make_image(fill_color="black", back_color="white")

        # Define the path for saving the QR code image
        qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'sale_{self.id}.png')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)

        # Save the image to the file system
        img.save(qr_code_path)

        # Update the qr_code field with the relative path
        self.qr_code = f'qrcodes/sale_{self.id}.png'

        # Save the updated object (this is the second save)
        super().save(*args, **kwargs)



class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale, models.DO_NOTHING, db_column='sale')
    product = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='product')
    price = models.FloatField()
    quantity = models.IntegerField()
    total_detail = models.FloatField()

    class Meta:
        db_table = 'SaleDetails'

    def __str__(self) -> str:
        return "Detail ID: " + str(self.id) + " Sale ID: " + str(self.sale.id) + " Quantity: " + str(self.quantity)

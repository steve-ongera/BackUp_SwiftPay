# sales/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sale
import qrcode
import os
from django.conf import settings
import random
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Sale

@receiver(post_save, sender=Sale)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        # QR code content
        qr_data = f"Sale ID: {instance.id}\nCustomer: {instance.customer}\nTotal: {instance.grand_total}\nDate: {instance.date_added}"
        
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

        # Define path to save QR code
        qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'sale_{instance.id}.png')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)

        # Save the image to the file system
        img.save(qr_code_path)

        # Update the Sale instance with the generated QR code
        instance.qr_code = f'qrcodes/sale_{instance.id}.png'
        instance.save()  # Save again to update the QR code field




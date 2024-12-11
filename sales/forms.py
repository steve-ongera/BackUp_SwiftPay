from django import forms
from .models import Sale, SaleDetail

class SaleForm(forms.ModelForm):
    """
    Form for updating a Sale object.
    """
    class Meta:
        model = Sale
        fields = '__all__'  # Include the fields you want to update

class SaleDetailForm(forms.ModelForm):
    """
    Form for updating SaleDetail objects if needed.
    """
    class Meta:
        model = SaleDetail
        fields = '__all__'  # Include the fields you want to update

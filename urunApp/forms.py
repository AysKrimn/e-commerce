from django import forms
from .models import *


# yorum düzenleme modeli
class EditComment(forms.ModelForm):
    class Meta:
        model=Yorumlar
        fields=['message']

        widget = {
        'message': forms.Textarea(attrs = 
         {
            'class': "form-control", 
            'placeholder': "Yorumunuz"        
        }),
        }

#  ürün olusturma modeli
class CreateUrun(forms.ModelForm):
    class Meta:
        model=Urun
        fields=['urunQRCode', 'ad', 'fiat', 'aciklama', 'resim']

        widgets = {
        'ad': forms.TextInput(attrs = {'class': "form-control" }),
        'urunQRCode': forms.TextInput(attrs = {'class': "form-control" }),
        'fiat': forms.TextInput(attrs = {'class': "form-control" }),
        'aciklama': forms.TextInput(attrs = {'class': "form-control" })
        }

        # help_texts = {

        # 'urunQRCode': "Ürünün stok kodu"

        # }

# kredi kartı oluşturma
class SaveCreditCard(forms.ModelForm):
    class Meta:
         model=CreditCardAccount
         fields=['cardNo', 'cardOwner', 'expiredMonthAndYear', 'cvc']
from django import forms
from .models import *

class CreateUrun(forms.ModelForm):
      class Meta:
            model=Urun
            fields=["ad", "urunDetayi", "fiat", "seriNo", "urunResmi"]


            help_texts = {
            
             'fiat': None

            }

# forum olustur
class EditComment(forms.ModelForm):
      class Meta:
            model=Yorum
            fields=['mesaj']


class CreditCardForm(forms.ModelForm):
      class Meta:
            model=UserCreditCard
            fields=['cardNo', 'cardOwner', 'expiredMonthAndYear', 'cvc']
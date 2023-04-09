from django import forms
from .models import *

class CreateUrun(forms.ModelForm):
      class Meta:
            model=Urun
            fields=["ad", "urunDetayi", "fiat", "seriNo", "urunResmi"]
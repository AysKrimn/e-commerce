from django.contrib import admin
from .models import *
# Modellerini admin sayfasında göster
admin.site.register(Urun)
admin.site.register(Yorumlar)
admin.site.register(CreditCardAccount)

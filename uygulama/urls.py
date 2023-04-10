"""ilkUygulama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

# view dosyasını import et
from urunApp.views import *
from userApp.views import *
# Dosyaları kayıt et
urlpatterns = [
    path('yonetici/', admin.site.urls),
    path("", index, name="anasayfa"),
    path("urun/<urunId>", urunDetay, name="urun-detay-sayfasi"),
    path("bulunamadi", hataSayfasi, name="hata-sayfasi"),
    path("urun-olustur", urunOlustur, name="urun-olustur"),
    path("yorumlar/<yorumId>", editComment, name="yorum-duzenle"),
    # user-login/register/signout
    path('kayit-ol', user_register, name="user-register"),
    path('giris-yap', user_login, name="user-login"),
    path('cikis-yap', user_logout, name="user-logout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""uygulama URL Configuration

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
# konfigürasyon dosyaları
from django.conf import settings
from django.conf.urls.static import static

# viewleri import
from urunApp.views import *
from userApp.views import *

urlpatterns = [
    path('yonetici/', admin.site.urls),
    path('', anasayfa, name="anasayfa"),
    path("urun/olustur", createProduct, name="create-product"),
    path('urun/<urunId>', detail_page, name="urun-detay-sayfasi"),
    path('urun/duzenle/<urunId>', editProduct, name="urun-duzenle"),
    path('urun/sil/<urunId>', deleteProduct, name="delete-product"),
    path('yorum-yap/<urunId>', makeComment, name="yorum-yap"),
    path('yorum-sil/gonderi/<urunId>/yorum/<yorumId>', deleteComment, name="yorum-sil"),
    path('yorum-duzenle/gonderi/<urunId>/yorum/<yorumId>', editComment, name="yorum-duzenle"),
    path('sayfa-bulunamadi', sayfa_bulunamadi, name="404"),
    # user-app burada başlar
    path('kayit-ol', user_register, name="user-register"),
    path('hesap', user_setting, name="user-setting"),
    path('giris-yap', user_login, name="user-login"),
    path('cikis-yap', user_logout, name="user-logout")
    # user-app burada biter

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

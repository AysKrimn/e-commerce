from django.db import models
from django.contrib.auth.models import User

# Veritanı modellerini oluştur
class Urun(models.Model):
    # database fields
    # textfield ve charfield mutlaka max-length belirtilmelidir
    # her class otomatik bir şekilde eklenen ürüne id atar
    olusturan = models.ForeignKey(User, verbose_name=("Ürünü Oluşturan"), on_delete=models.CASCADE, default=1)
    ad = models.CharField(("Ürünün Adı"), max_length=50)
    fiat = models.CharField(("Ürünün Fiatı"), max_length=6)
    aciklama = models.TextField(("Ürünün Açıklaması"),  max_length=200, default="Detay Belirtilmedi...")
    urunQRCode = models.CharField(("Ürünün QR Kod Numarası"), max_length=10, null=True, blank=True)
    eklendi = models.DateTimeField(("Eklendi"), auto_now_add=True)
    garanti = models.BooleanField(("Garantisi Var Mı"), default=True, help_text="Ürünün garantisi")
    stok = models.IntegerField(("Stok Sayısı"), default=1, help_text="Ürünün Stok Sayısı")
    # rating
    # ürünü satan firma
    # ürünü satışa sunan kişi
    resim = models.FileField(("Resim"), upload_to="uploads", default="../static/public/no-image.jpg", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.ad
    # veritabanına yeni bir veri eklendiginde veritabanını güncellemeyi unutma 
    # ayarla
    def garantiSorgula(self):
        garanti = self.garanti
        if garanti:
            return "Var"
        else:
            return "Yok"

    # resim ayarla
    def resimAyarla(self):
        resim = self.resim
        if resim:
            return resim
        else:
            # statik dosyayı döndür
            return "../static/public/no-image.jpg"
        



    # yorum alanı
class Yorumlar(models.Model):
    # tabloları birleştir
    urun = models.ForeignKey(Urun, verbose_name=("Ürün"), on_delete=models.CASCADE, related_name="yorumlar")
    yazar = models.ForeignKey(User, verbose_name=("Yazar"), on_delete=models.CASCADE)
    tarih = models.DateTimeField(auto_now_add=True)
    message = models.TextField(("Yorum"), max_length=100)

    def __str__(self):
        return "{user} {product} ürüne yorum yaptı".format(user=self.yazar, product=self.urun.ad)



# User Credit Card
class CreditCardAccount(models.Model):
    user = models.ForeignKey(User, verbose_name=("Hesap Sahibi"), on_delete=models.CASCADE)
    cardNo = models.CharField(("Kart Numarası"), max_length=19)
    cardOwner = models.CharField(("Kart Sahibi"), max_length=20)
    expiredMonthAndYear = models.CharField(("Son Kullanım Tarihi"), max_length=4)
    cvc = models.CharField(("Güvenlik Kodu"), max_length=3)

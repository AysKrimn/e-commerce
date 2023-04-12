from django.db import models


# Veritanı modellerini oluştur
class Urun(models.Model):
    # database fields
    # textfield ve charfield mutlaka max-length belirtilmelidir
    # her class otomatik bir şekilde eklenen ürüne id atar
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
    # veritabanına yeni bir veri eklendiginde veritabanını güncellemeyi unutma !
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
    yazar = models.CharField(("Yorumu Yapan Kişi"), max_length=50)
    tarih = models.DateTimeField(auto_now_add=True)
    message = models.TextField(("Yorum"), max_length=100)

    def __str__(self):
        return "{user} {product} ürüne yorum yaptı".format(user=self.yazar, product=self.urun.ad)


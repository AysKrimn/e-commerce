from django.db import models

# veritabanı modelleri

class Urun(models.Model):
    # database fields
    # django her class için otomatik id fieldi atar
    ad = models.CharField(("Ürünün adı"), max_length=50)
    urunDetayi = models.TextField(verbose_name="Ürün hakkında açıklama", max_length=200)
    eklenmeTarihi = models.DateTimeField(auto_now_add=True)
    fiat = models.CharField(("Ürünün Fiatı"), default="Ücret Belirtilmedi", max_length=6, help_text="Ürünün ücretidir")
    seriNo = models.CharField(("Ürünün Seri Numarası"), max_length=7, null=True, blank=True)
    urunResmi = models.FileField(("Ürünün Resmi"), upload_to="uploads", max_length=100, null=True, blank=True)
    stokAdet = models.PositiveIntegerField(("Stoktaki Adet Sayısı"), default=1)
    garanti = models.BooleanField(("Garanti"), default=False)
    # sahibi

    # meta verisi
    def __str__(self):
        return "{ad} | {ürünFiat}".format(ad=self.ad, ürünFiat=self.fiat)
    
    def seriNumarasiKontrol(self):
        if self.seriNo:
            return self.seriNo
        else:
            return "Kayıt Edilmemiş"

    # garanti varmı yokmu
    def garantiKontrol(self):
        if self.garanti:
            return "Var"
        else: 
            return "Yok"

    def stokKontrol(self):
        if self.stokAdet > 0:
            return "{miktar} adet".format(miktar=self.stokAdet)
        elif self.stokAdet == 0:
            return "Tükendi"
        
    def resimKontrol(self):
        if self.urunResmi:
            return self.urunResmi
        else:
            return "static/public/noimg.jpg"
        


# yorum modeli
class Yorum(models.Model):
    product = models.ForeignKey(Urun, verbose_name=("Ürün"), on_delete=models.CASCADE, related_name="yorumlar", default="")
    yazar = models.CharField(("Yazar"), max_length=50)
    mesaj = models.TextField(("Mesaj"), max_length=350)
    olusturuldu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.yazar
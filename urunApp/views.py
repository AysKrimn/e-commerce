from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
# Ürün modelini dahil et
from .models import *


# Sayfalarımızı burada hazırlarız
def index(request):
    context = {}
    # veritabanı sorgusu başlat verileri döndür ve index.html de yazdır
    # Djangonun ORM yapısı
    urunler = Urun.objects.all().order_by("-eklendi")  # veritabanındaki tüm ürünleri getirir
    # context'e kayıt et
    context["data"] = urunler # { data: urunler }

    # urunler queryset (array) 
    return render(request, 'index.html', context)

# hata sayfası
def hataSayfasi(request):
    return render(request, '404.html')


# ürün detay sayfası
def checkPost(id):
    try:
      urun = Urun.objects.get(id=id)
      return urun
    except:
        return False

# @login_required(login_url='user-login')
def urunDetay(request, urunId):
    # vertabanı sorgusu başlat
    context = {}

    if request.method == "POST":
        # metot post ise
        urun = checkPost(urunId) # urun veya false gelecek
        if urun:
            # yorum içeriğine bir şeyler gönder
            message = request.POST.get('message')
            urun.yorumlar.create(yazar=request.user, message=message).save()
            # bir sayfaya yönlendir
            return redirect('/urun/' + urunId)
    else:
        # get isteği
        # Hata ayıklama
        urunKontrol = checkPost(urunId)
        if urunKontrol:
            context['data'] = urunKontrol
        else:
            # urunKontrol false ise
              return redirect('hata-sayfasi')

        return render(request, 'product_detail.html', context)


# ürün oluşturma sayfası
from .forms import CreateUrun
def urunOlustur(request):
    # eğer bana post isteği gelmişse
    if request.method == "POST":
        form = CreateUrun(request.POST, request.FILES)
        # formu kontrol et
        if form.is_valid():
          form.save()

        return redirect('anasayfa')
    
    else:
        # get/put/delete işlemleri
      form = CreateUrun()
      return render(request, 'createProduct.html', {'form': form})

# ürün düzenleme sayfasi vs


# yorum düzenleme sayfasi
from .forms import EditComment
def editComment(request, urunId, yorumId):
    context = {}
    yorum = Yorumlar.objects.filter(id=yorumId).first() # {} döndürür

    if yorum is None:
        # sessiona mesaj gönder
        messages.warning(request, message="Üzgünüz... Aradığınız şeyi anlayamadık.")
        return redirect("hata-sayfasi")
    
    if yorum.yazar.id != request.user.id:
        raise PermissionDenied()

    if request.method == 'POST':
        # veritabanına gönder
        form = EditComment(request.POST, instance=yorum)
        # verileri oluştur
        if form.is_valid():
            comment = form.save(commit=False) # modelin tüm kalıtımlarını verecek
            comment.urun = yorum.urun
            # veritabanını kayıt et
            comment.save() 
        # yönlendir
        return redirect('/urun/' + str(yorum.urun.id))
    else:
        # get metodu gelirse çalışacak
        # contextle beraber gönder
        duzenle = EditComment(instance=yorum)
        context['data'] = yorum
        context['form'] = duzenle
        return render(request, "editComment.html", context)
    

# yorum sil (API)
def deleteComment(request, urunId, yorumId):
        
        yorum = Yorumlar.objects.filter(id=yorumId).first() # {} döndürür
        # eğer yoksa
        if yorum is None:
            messages.warning(request, message="Üzgünüz... Böyle bir yorum bulamadık.")
            return redirect('hata-sayfasi')
        # yetkisi yoksa
        if yorum.yazar.id != request.user.id:
           raise PermissionDenied()
        
        # yorumu sil
        yorum.delete()
        return redirect('/urun/' + str(urunId))
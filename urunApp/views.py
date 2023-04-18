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
        
        # isteği yapan kişi ürünü oluşturan kişi ise
        if urunKontrol.olusturan.id == request.user.id:
            context['productOwner'] = True
        # isteği yapan kişi adminse
        if request.user.is_superuser:
            context['admin'] = True
        

        return render(request, 'product_detail.html', context)


# ürün oluşturma sayfası
from .forms import CreateUrun
def urunOlustur(request):
    # eğer kişi kayıtlı değilse
    if request.user.is_authenticated is not True:
        return redirect('user-login')
    
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
def urunDuzenle(request, urunId):
    # post, get
    context = {}
    urun = Urun.objects.filter(id=urunId).first() 

    if urun is None:
        return redirect('hata-sayfasi')
    
    # postu yalnızca oluşturan kişi ya da bir admin düzenleyebilir.
    if urun.olusturan.id != request.user.id and request.user.is_superuser is not True:
         raise PermissionDenied()
    
    context['data'] = urun
    context['form'] = CreateUrun(instance=urun)

    if request.method == 'POST':
        # requestten gelen postu ve fieldi al
        urunForm = CreateUrun(request.POST, request.FILES, instance=urun)
        if urunForm.is_valid():
            # veritabanına kayıt-et
            urunForm.save()
            # urunun sayfasına gönder
            return redirect('/urun/' + str(urunId))
    else:
        return render(request, 'editProduct.html', context)

# ürün silme sayfası
def urunSil(request, urunId):
        
        urun = Urun.objects.filter(id=urunId).first()

        if urun:
            urun.delete()
            # session mesaj gönder
            return redirect('anasayfa')
        
        else:
            return redirect('hata-sayfasi')
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
        if yorum.yazar.id != request.user.id and request.user.is_superuser is not True:
           raise PermissionDenied()
        
        # yorumu sil
        yorum.delete()
        messages.success(request, 'Başarılı bir şekilde yorum silindi')
        return redirect('/urun/' + str(urunId))
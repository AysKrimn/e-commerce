from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# sayfalarımızın ayarlandığı yer 
def anasayfa(request):
    context = {}
    butunVeriler = Urun.objects.all().order_by("-eklenmeTarihi")   # queryset array
    # context içine at
    context["data"] = butunVeriler

    # sayfayı render et
    return render(request, 'index.html', context)

# hata sayfası
def sayfa_bulunamadi(request):
     return render(request, '404.html')

# detay sayfası 
def detail_page(request, urunId):
    # veritabanı sorgulaması
    context = {}
    try:
          urun = Urun.objects.get(id=urunId) # bulursa object aksi taktirde güzel bir hata 
          context['data'] = urun
          # kredi kartı var mı yok mu?
          hasCard = UserCreditCard.objects.filter(user=request.user).first()
    
          if hasCard:
              context['hasCard'] = True
          else: 
              context['hasCard'] = False   
          # user adminse
          if request.user.is_superuser:
              context['admin'] = True
          # user ürünü oluşturan kişi ise
          if request.user.id == urun.satici.id:
              context['urunSahibi'] = True

    except:
       return redirect('404')
          
    return render(request, 'detail_product.html', context)

# ürün ekleme
from .form import CreateUrun
def createProduct(request):
     # metotları ayır
     context = {}
     urunForm = CreateUrun()
     if request.method == "POST":
          # post isteği için
          urunForm = CreateUrun(request.POST, request.FILES)
          # REQUEST FILES CALİSMİYOR
          if urunForm.is_valid():
              urunForm.save()

          # anasayfaya yönlendir
          return redirect('anasayfa')
     
     else:
      # get put delete istekleri için:
      context['form'] = urunForm
      return render(request, 'createProduct.html', context)

#ürün güncelle
def editProduct(request, urunId):
    context = {}
    
    urun = Urun.objects.filter(id=urunId).first()
 
    if urun is None:
        return redirect('404')
    
    if urun.satici.id != request.user.id and request.user.is_superuser is not True:
        raise PermissionDenied()
    
    productForm = CreateUrun(instance=urun)

    if request.method == 'POST':
        urunForm = CreateUrun(request.POST, request.FILES, instance=urun)
        if urunForm.is_valid():
            urunForm.save()
        # sayfaya yönlendir
        return redirect("/urun/" + str(urunId))
    else:
        # get istekleri
        context['form'] = productForm
        context['data'] = urun
        return render(request, 'editProduct.html', context)
    

# ürün sil
def deleteProduct(request, urunId):
    # get isteği geldiğinde mesajı sil
    product = Urun.objects.filter(id=urunId).first()

    if product is None:
        return redirect('404')
    
    # isteği yapan kişi?
    if product.satici.id != request.user.id and request.user.is_superuser is not True:
        # permission denied
         raise PermissionDenied()
    
    # hiçbir problem yoksa veriyi sil
    product.delete()
    return redirect('anasayfa')


# yorum yapma (API)
def makeComment(request, urunId):
     # ürünü bul
     if request.method == 'POST':
         
          urun = Urun.objects.get(id=urunId)
          if urun:
            # dataları çek
            message = request.POST.get('message')
            # author ve message urunün yorum kısmına kayıt et
            urun.yorumlar.create(yazar=request.user, mesaj=message).save()  
            # ürünün sayfasına yönlendir
            return redirect('/urun/' + str(urunId)) 
          else:
               # hata sayfasına yönlendir 
              return redirect('404') 
     else:
       # get istekleri için
        return redirect('/urun/' + str(urunId)) 


# yorum düzenleme
from .form import EditComment
def editComment(request, urunId, yorumId):
    context = {}
    yorum_data =  Yorum.objects.filter(id=yorumId).first()

    if yorum_data is None:
     # bulunamadı sayfasına yönlendir.
        return redirect('404')
    
     # 3. kişi manipule etmeye çalışıyorsa ve bu kişi admin değilse
    if request.user.id != yorum_data.yazar.id and request.user.is_superuser is not True:
         raise PermissionDenied()
    
     # kontroller, güvenlik ve get,fitler farki    
    if request.method == "POST":
        editForm = EditComment(request.POST, instance=yorum_data)
        if editForm.is_valid():
            #  veritabanini güncelle
            editForm.save()
        
        # yorumun oldugu yere yönlendir
        return redirect("/urun/" + str(urunId))
    
    else:
        # get istegi gelirse
        context['productId'] = urunId
        context['commentId'] = yorumId
        context['form'] = EditComment(instance=yorum_data)
        return render(request, 'comment/edit_comment.html', context)
    
# yorum silme (API)
def deleteComment(request, urunId, yorumId):

    yorum_data = Yorum.objects.filter(id=yorumId).first()

    if yorum_data is None:
        return redirect('404')
    
    if request.user.id != yorum_data.yazar.id and request.user.is_superuser is not True:
         raise PermissionDenied()
    # yorumu sil
    yorum_data.delete()
    # sayfaya yönlendir
    # session messages
    messages.success(request, 'Başarılı bir şekilde mesaj silindi.')
    return redirect('/urun/' + str(urunId))
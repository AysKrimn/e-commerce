from django.shortcuts import render, redirect
from .models import Urun


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
          print("yorum:", urun.yorumlar.all())
                         # contexte at
          context['data'] = urun
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



# yorum yapma (API)
def makeComment(request, urunId):
     # ürünü bul
     if request.method == 'POST':
         
          urun = Urun.objects.get(id=urunId)
          if urun:
            # dataları çek
            author = request.POST.get('author')
            message = request.POST.get('message')
            # author ve message urunün yorum kısmına kayıt et
            urun.yorumlar.create(yazar=author, mesaj=message).save()  
            # ürünün sayfasına yönlendir
            return redirect('/urun/' + str(urunId)) 
          else:
               # hata sayfasına yönlendir 
              return redirect('404') 
     else:
       # get istekleri için
        return redirect('/urun/' + str(urunId)) 


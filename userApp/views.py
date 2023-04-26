from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from urunApp.models import UserCreditCard
# Create your views here.

# user kayıt olursa
def user_register(request):

    if request.method == 'POST':
        
        k_ad = request.POST.get('k_ad')
        k_email = request.POST.get('k_email')
        k_sifre = request.POST.get('k_sifre')

        if k_ad and k_email and k_sifre:
            # veritabanını sorgula
            try:
              User.objects.get(email = k_email)
              # böyle bir kullanıcı varsa hata mesajı döndür
              messages.error(request, message="Bu email adresine sahip bir hesap mevcut")
              return redirect('user-register')  
            except:
              # böyle bir kullanıcı yoktur o zaman kayıt et 
               User.objects.create_user(username=k_ad, email=k_email, password=k_sifre)
               #  başarılı measjı ver
               messages.success(request, message='Başarılı bir şekilde kayıt oldunuz. Lütfen giriş yapın.')
               return redirect('user-login')  
    
    else:
      return render(request, 'user-register.html')


# user giriş yaparsa
def user_login(request):

    if request.method == "POST":
        k_ad = request.POST.get('k_ad')
        k_sifre = request.POST.get('k_sifre')

        if k_ad and k_sifre:
           user = authenticate(request, username=k_ad, password=k_sifre)

           if user is not None:
              login(request, user)
              # ansayfaya yönlendir
              return redirect('anasayfa')
           else:
              # hata mesajı yazdır ve logine yönlendir
              messages.error(request, message='kullanıcı adı veya parola hatalı')
              return redirect('user-login')
    
    else:
       # get isteği geldiğinde sayfayı gönder
       return render(request, 'user-login.html')
    

# çıkış yapma
def user_logout(request):

        logout(request)
        # anasayfaya yönlendir
        return redirect('anasayfa')
# hesap ayarları
from urunApp.form import CreditCardForm
def user_setting(request):
    context = {}
    cardForm = CreditCardForm()
    # kullanıcının kartı varmı  yokmu
    hesapBilgisi = UserCreditCard.objects.filter(user=request.user).first()
    
    if hesapBilgisi is None:
        context['cardDetail'] = False
    else:
        context['cardDetail'] = hesapBilgisi
        context['form'] = CreditCardForm(instance=hesapBilgisi)

    # post isteği gelirse
    if request.method == 'POST':

        duzenlemeIstegi = request.POST.get('_cardDuzenle')
        sifreDegistirmeIstegi = request.POST.get('_sifreDuzenle')

        if sifreDegistirmeIstegi:
            # şifre değiştirme isteği gelmiş inputları al
            sifre_1 = request.POST.get('password_check_1')
            sifre_2 = request.POST.get('password_check_2')

            if sifre_1 and sifre_2 and sifre_1 == sifre_2:
                # user objesini bul
                user = User.objects.filter(id=request.user.id).first()
                # şifre değiş
                user.set_password(sifre_1)
                user.save()
                # çıkış yap ve tekrar girmesini iste
                logout(request)
                return redirect('user-login')

        # düzenleme isteği varsa kart bilgilerini güncelle
        if duzenlemeIstegi:
            cardForm = CreditCardForm(request.POST, instance=hesapBilgisi)
            if cardForm.is_valid():
                cardForm.save()
                messages.success(request, message="Başarılı bir şekilde kart bilgileriniz güncellendi.")
                return redirect('user-setting')
            else:
                # potansiyel hata durumlarında
                messages.error(request, message='Üzgünüz kartınızı güncellerken bir takım sorunlar meydana geldi. Daha sorna tekrar dene.')
                return redirect('404')
            
        # düzenleme isteği yoksa alt koşulu çalıştır:
        # POST ÜZERİNDEN VERİLERİ ÇEK (KARTI YOKSA KART OLUŞTUR)
        cardForm = CreditCardForm(request.POST)
        if cardForm.is_valid():
            cardForm = cardForm.save(commit=False)
            cardForm.user = request.user
            cardForm.save()
            return redirect('user-setting')
        else:
            print('hatalar:', cardForm.errors.as_data())
            messages.error(request, message='Üzgünüz kartınızı oluştururken bir takım sorunlar meydana geldi. Daha sorna tekrar dene.')
            return redirect('404')
    else:
     # get istekleri
     return render(request, 'user-setting.html', context)
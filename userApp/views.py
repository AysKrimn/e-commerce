from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# credicardaccount modeli
from urunApp.models import CreditCardAccount


# user kayıt olursa
def user_register(request):

    if request.method == 'POST':
        # verileri çek
        # veritabanına işle
        k_ad = request.POST.get('k_ad')
        k_email = request.POST.get('k_email')
        k_sifre = request.POST.get('k_sifre')

        if k_ad and k_email and k_sifre:
            # sorgulama işlemleri
            try:
                User.objects.get(email=k_email)
                # hata mesajı verdir
                messages.error(request, message="Bu email adresine sahip bir kullanıcı zaten mevcut") 
                return redirect('user-register')
            except User.DoesNotExist:
                # böyle bir kullanıcı yoktur kayıt et
                User.objects.create_user(username=k_ad, email=k_email, password=k_sifre)
                messages.success(request, 'Başarılı bir şekilde kayıt oldunuz. Lütfen giriş yapın.')
                # gir yapmaya yönlendir
                return redirect('user-login')
            

    else:
        return render(request, 'user-register.html')



# user giriş yapmaya çalışırsa
def user_login(request):

    if request.method == 'POST':
        k_ad = request.POST.get('k_ad')
        k_sifre = request.POST.get('k_sifre')

        if k_ad and k_sifre:
            user = authenticate(request, username=k_ad, password=k_sifre)

            if user is not None:
                # giriş yaptır
                login(request, user)
                return redirect('anasayfa')
            else:
                messages.error(request, 'Kullanıcı adı veya parola hatalı')
                return redirect('user-login')
    else:
       # eğer kullanıcı zaten login olmuşsa    
       if request.user.is_authenticated:
           return redirect('anasayfa')
       else:           
          return render(request, 'user-login.html')
    

# user çıkış yaparsa
def user_logout(request):
    # giriş yapmayan kullanıcıları engelle
    if request.user.is_authenticated:
        logout(request)
        return redirect('anasayfa')
    else:
        return redirect('anasayfa')
    

# hesap ayarları
from urunApp.forms import SaveCreditCard
def user_setting(request):
      context = {}
      cardForm = SaveCreditCard()
      paymentDetail = CreditCardAccount.objects.filter(user=request.user).first()

      if paymentDetail is None:
        context['cardDetail'] = False
      else:
          context['cardDetail'] = paymentDetail
          context['cardForm'] = SaveCreditCard(instance=paymentDetail)


      # post isteği atılmışsa
      if request.method == 'POST':
          # form üzerinden gönderilen bütün verilere ulaş  
          kartGuncellemeIstegi = request.POST.get('_kart_guncelle')
          print("GUNCELLEME İSTEGİ:", kartGuncellemeIstegi)

          if kartGuncellemeIstegi:
            cardForm = SaveCreditCard(request.POST, instance=paymentDetail)
            if cardForm.is_valid():
                cardForm.save()
            else:
                print(cardForm.errors.as_text())
            # session mesaj gönder vs
            return redirect('user-setting')
          
          else:
            # Kart düzenleme değilse 
            cardForm = SaveCreditCard(request.POST)
            if cardForm.is_valid():
                # form validation (doğrulanmasında hata olmadıysa)
                cardForm = cardForm.save(commit=False)
                cardForm.user = request.user
                # şimdi kayıt-et
                cardForm.save()
                return redirect('user-setting')
            
            else:
                # formda herhangi bir validation hatası meydana gelirse
                print(cardForm.errors.as_text())
                # hata meydana geldi ne istersen onu yap
                return redirect('hata-sayfasi')  
      
      else:
         # get istekleri
         return render(request, 'user-settings.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
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
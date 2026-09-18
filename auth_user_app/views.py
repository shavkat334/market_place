from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        print(user)

        if user is None:
            return redirect("auth_user_app:login_page")

        login(request, user)
        print("Login qilindi !")
        return redirect("main:home_page")


    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("auth_user_app:login_page")

# Categoriya modelini
# Products modelini shakllantirib
# aososiy sahifada product listingni amalga oshririb kelaslar 

# cart funksionalligi ,ordering qilip kelselar bolaveradi 


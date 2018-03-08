from django.shortcuts import render
from django.contrib.auth import authenticate,login


# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST.get("email","")
        pass_word = request.POST.get("password","")
        user = authenticate(email,pass_word)
        if user is not None:
            login(request,user)
            return render(request,"wellcomepage.html")
    elif request.method == "GET":
        return render(request,"login.html",{})
from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from useraccount.forms import UserRegisterForm,UserLoginForm
from django.views import View
from django.contrib import messages





def user_register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form=UserRegisterForm()
    return render(request,'register.html',{'form':form})

class UserLogin(View):
    def post(self,request,*args,**kwargs):
        form=UserLoginForm(request.POST)
        if form.is_valid():
            password=request.POST.get("password")
            email=request.POST.get("email")
            user=authenticate(email=email,password=password)   
            if user:
                login(request,user)
                messages.add_message(request,messages.INFO,"Login Successfull !! ")
                return redirect("product:home")
        return render(request,"login.html",{"form":form})

            
            
    def get(self,request,*args,**kwargs):
        form=UserLoginForm()
        return render(request,"login.html",{"form":form})
        
        
  
def user_logout(request):
    logout(request)
    return redirect("product:home")
    

    
    
    
    
    



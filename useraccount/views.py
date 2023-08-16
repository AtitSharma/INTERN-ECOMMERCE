from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from useraccount.forms import UserRegisterForm,UserLoginForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from useraccount.models import User,Token
from django.conf import settings
from django.core.mail import send_mail
        
        
def send_mail_to_user(email): 
    user=User.objects.get(email=email)
    user_id =user.id
    user_token=Token.objects.create(user=user)
    subject="Verifyyy"
    message=f"Verify Your Email in  http://localhost:8000/user/verify/{user_token}  Dont share this link to anyone"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email] 
    send_mail(subject,message,from_email,recipient_list)    



def user_register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        email=request.POST.get("email")
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            send_mail_to_user(email=email)
            return redirect('product:home')
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
    
    

   
class PasswordChange(PasswordChangeView):
    success_url=reverse_lazy("product:home")
    template_name="password_change.html"
    
    
   
class VerifyTokenView(View):
    def get(self,request,*args,**kwargs):
        token=self.kwargs.get("token")
        user_token=Token.objects.filter(key=token).first()
        if user_token:
            user=user_token.user
            user.is_active=True
            user.save()
            messages.add_message(request,messages.INFO,"Successfully Verified Procceed To Login")
            return redirect("product:home")
        messages.add_message(request,messages.INFO,"Verification Failed ")
        return redirect("product:home")  
   
#


    



from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate,get_user_model
from useraccount.forms import UserRegisterForm,UserLoginForm
from django.views import View
from . tokens import AccountActiveTokenGenerator
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage



def activate(request,uidb64,token):
    User=get_user_model()
    
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except :
        user=None
        
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Succesfully Verified !! Proceed To Login !!!")
        return redirect("user:login")
    else:
        messages.error(request,"Activation Link Invalid !!! ")
        
    return redirect("product:home")




def activateEmail(request,user,to_email):
    mail_subject="Activate Your User Account"
    message=render_to_string("template_active_account.html",{
        "user":user.username,
        "domain":get_current_site(request).domain,
        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        "token":account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http',
        
        
        
    })
    email=EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
        messages.success(request,f"Dear user {user.username} check you email {to_email} <br> And Verify !!!")
        return redirect("product:home")
    else:
        messages.error(request,f"Problem Sending The Email !! to {to_email}")
        return redirect("product:home")
        
        
    



def user_register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request,user,form.cleaned_data.get("email"))
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
    

    
    
    
    
    



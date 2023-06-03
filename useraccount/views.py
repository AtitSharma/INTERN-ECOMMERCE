from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from useraccount.forms import UserRegisterForm



def user_register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form=UserRegisterForm()
    return render(request,'register.html',{'form':form})

class UserLogin(LoginView):
    template_name='login.html'
    
  
def user_logout(request):
    logout(request)
    return redirect("product:home")
    

    
    
    
    
    



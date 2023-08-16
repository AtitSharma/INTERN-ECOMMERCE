from django.urls import path
from useraccount.views import UserLogin,user_register,user_logout,PasswordChange,VerifyTokenView
app_name='user'
urlpatterns = [
    path("login/",UserLogin.as_view(),name="login"),
    path('register/',user_register,name='register'),
    path('logout/',user_logout,name="logout"),
    path("verify/<token>",VerifyTokenView.as_view(),name="activate"),
    path("change_password/",PasswordChange.as_view(),name="password_change")
    
]

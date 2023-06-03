from django.urls import path
from useraccount.views import UserLogin,user_register,user_logout
app_name='user'
urlpatterns = [
    path("login/",UserLogin.as_view(),name="login"),
    path('register/',user_register,name='register'),
    path('logout/',user_logout,name="logout")
    
]

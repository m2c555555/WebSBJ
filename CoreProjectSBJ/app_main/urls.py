from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path
from . import views



def login_redirect(request):
    return redirect('social:begin', 'line')

def logout_view(request):
    logout(request)
    return redirect('/')  # หลัง Logout ให้ Redirect ไปหน้าแรก

urlpatterns = [
    path('', views.main, name='main'),
    #path('line/complete/line', views.line_callback, name='line_callback'),
    path('line/complete/line/', views.line_callback, name='line_callback'),
    path('line/', include('social_django.urls', namespace='social')),  # ดึง path ของ social-auth
    path('logout/', logout_view, name='logout'),
    path('main/', login_redirect, name='line_login'),
]

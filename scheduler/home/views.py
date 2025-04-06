from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_staff:
        return redirect('task_list')
    else:
        return redirect('inquiry_list')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {'error_message': '아이디 또는 비밀번호가 올바르지 않습니다.'})
    return render(request, "login.html")

def logout_view(request):
    auth_logout(request)
    return redirect('login')
    

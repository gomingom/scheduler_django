from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import User
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {
                'error_message': '아이디 또는 비밀번호가 올바르지 않습니다.',
                'username': username  # 사용자가 입력한 username 유지
            })
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect('login')

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, "create_user.html")
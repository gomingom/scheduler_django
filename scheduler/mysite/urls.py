"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from inquiries.views import (
    inquiry_list,
    inquiry_detail,
    inquiry_create,
    inquiry_update,
    inquiry_delete,
)
from tasks.views import (
    task_list,
    task_detail,
    task_create,
    task_update,
    task_delete,
)
from users.views import login_user, logout_user
from home.views import home
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("admin/", admin.site.urls),
    path("inquiries/", inquiry_list, name="inquiry_list"),
    path("inquiries/<int:pk>/", inquiry_detail, name="inquiry_detail"),
    path("inquiries/create/", inquiry_create, name="inquiry_create"),
    path("inquiries/<int:pk>/update/", inquiry_update, name="inquiry_update"),
    path("inquiries/<int:pk>/delete/", inquiry_delete, name="inquiry_delete"),
    path("tasks/", task_list, name="task_list"),
    path("tasks/<int:pk>/", task_detail, name="task_detail"),
    path("tasks/create/", task_create, name="task_create"),
    path("tasks/<int:pk>/update/", task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", task_delete, name="task_delete"),
]

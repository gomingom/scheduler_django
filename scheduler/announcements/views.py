from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Announcement
from .forms import AnnouncementForm


def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, "announcements/announcement_list.html", {"announcements": announcements})


def announcement_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to create announcements.")
    
    if request.method == "POST":
        form = AnnouncementForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("inquiry_list")
    return render(request, "announcements/announcement_create.html", {"form": AnnouncementForm(user=request.user)})

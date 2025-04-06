from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Inquiry
from .forms import InquiryForm
from users.models import User


# Create your views here.
def inquiry_list(request):
    inquiries = Inquiry.objects.all()
    return render(request, "inquiry_list.html", {"inquiries": inquiries})


def inquiry_detail(request, pk):
    inquiry = Inquiry.objects.get(pk=pk)
    return render(request, "inquiry_detail.html", {"inquiry": inquiry})


def inquiry_create(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect("inquiry_list")
        else:
            print(form.errors)
            return HttpResponse(form.errors.as_json())
    return render(request, "inquiry_create.html", {"form": InquiryForm()})


def inquiry_update(request, pk):
    inquiry = Inquiry.objects.get(pk=pk)
    if request.method == "POST":
        form = InquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            return redirect("inquiry_list")
    return render(
        request, "inquiry_update.html", {"form": InquiryForm(instance=inquiry)}
    )


def inquiry_delete(request, pk):
    inquiry = Inquiry.objects.get(pk=pk)
    inquiry.delete()
    return redirect("inquiry_list")

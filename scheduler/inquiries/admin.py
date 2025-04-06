from django.contrib import admin
from .models import Inquiry


# Register your models here.
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "ship_name",
        "block_name",
        "inquirer",
        "request_date",
        "is_accepted",
    )

from django.db import models
from inquiries.models import Inquiry
from users.models import User


# Create your models here.
def report_upload_path(instance, filename):
    # 예: reports/년도/월/작업ID_파일명
    return f'reports/{instance.work_date.year}/{instance.work_date.month}/{instance.id}_{filename}'

class Task(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, null=True, blank=True)
    ship_name = models.CharField(max_length=100, null=True, blank=True)
    block_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    work_date = models.DateField()
    work_time = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    report_file = models.FileField(upload_to=report_upload_path, null=True, blank=True)


    def __str__(self):
        if self.inquiry:
            return f"{self.inquiry.ship_name} - {self.inquiry.block_name}"
        else:
            return f"{self.ship_name} - {self.block_name}"

from django.db import models
from inquiries.models import Inquiry
from users.models import User


# Create your models here.
class Task(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    description = models.TextField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    work_date = models.DateField()
    work_time = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.inquiry.ship_name} - {self.inquiry.block_name}"

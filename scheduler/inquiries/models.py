from django.db import models
from users.models import User


# Create your models here.
class StatusChoices(models.TextChoices):
    PENDING = "대기", "대기"
    ACCEPTED = "승인", "승인"
    REJECTED = "반려", "반려"
    CANCLED = "취소", "취소"

class DeviceChoices(models.TextChoices):
    DEVICE_1 = "일반측정", "일반측정"
    DEVICE_2 = "3D Scanner", "3D Scanner"

class Inquiry(models.Model):
    ship_name = models.CharField(max_length=150)
    block_name = models.CharField(max_length=150)
    inquirer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=150, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    device = models.CharField(max_length=150, choices=DeviceChoices.choices)
    inquiry_detail = models.TextField()
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.ship_name} - {self.block_name}"

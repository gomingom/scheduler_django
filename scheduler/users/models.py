from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    email = models.EmailField(editable=False)
    name = models.CharField(max_length=150, editable=True, default="")
    group = models.CharField(max_length=150, editable=True, default="", null=True)
    is_staff = models.BooleanField(default=False)
    contact_number = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^01[016789][0-9]{7,8}$',
                message='올바른 핸드폰 번호 형식이 아닙니다. (예: 01012345678)'
            )
        ]
    )
    

    def __str__(self):
        return self.username

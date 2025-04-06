from django import forms
from .models import Inquiry, StatusChoices
from users.models import User


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["ship_name", "block_name", "inquirer", "request_date", "status"]
        widgets = {
            "request_date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.Select(choices=StatusChoices.choices),
            "inquirer": forms.Select(choices=User.objects.all()),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

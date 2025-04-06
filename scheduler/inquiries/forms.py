from django import forms
from .models import Inquiry, StatusChoices
from users.models import User


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["ship_name", "block_name", "request_date", "status"]
        widgets = {
            "request_date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.Select(choices=StatusChoices.choices),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.inquirer = self.user
        if commit:
            instance.save()
        return instance

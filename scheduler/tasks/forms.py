from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["inquiry", "description", "manager", "work_date", "work_time"]
        widgets = {
            "work_date": forms.DateInput(attrs={"type": "date"}),
            "work_time": forms.Select(
                choices=[
                    ("", "시간 선택"),
                    ("오전 1", "오전 1시"),
                    ("오전 2", "오전 2시"),
                    ("오전 3", "오전 3시"),
                    ("오전 4", "오전 4시"),
                    ("오전 5", "오전 5시"),
                    ("오전 6", "오전 6시"),
                    ("오전 7", "오전 7시"),
                    ("오전 8", "오전 8시"),
                    ("오전 9", "오전 9시"),
                    ("오전 10", "오전 10시"),
                    ("오전 11", "오전 11시"),
                    ("오전 12", "오전 12시"),
                    ("오후 1", "오후 1시"),
                    ("오후 2", "오후 2시"),
                    ("오후 3", "오후 3시"),
                    ("오후 4", "오후 4시"),
                    ("오후 5", "오후 5시"),
                    ("오후 6", "오후 6시"),
                    ("오후 7", "오후 7시"),
                    ("오후 8", "오후 8시"),
                    ("오후 9", "오후 9시"),
                    ("오후 10", "오후 10시"),
                    ("오후 11", "오후 11시"),
                    ("오후 12", "오후 12시"),
                ]
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        # 작업 요청 필드의 선택 옵션을 ship_name - block_name 형식으로 표시
        self.fields["inquiry"].label_from_instance = (
            lambda obj: f"{obj.ship_name} - {obj.block_name}"
        )

        # 담당자 필드의 선택 옵션을 username으로 표시
        self.fields["manager"].label_from_instance = lambda obj: obj.username

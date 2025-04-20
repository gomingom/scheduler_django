from django import forms
from .models import Task
from users.models import User
from inquiries.models import Inquiry

class TaskForm(forms.ModelForm):
    INQUIRY_STATUS_CHOICES = [
        ('pending', '대기중'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    inquiry_status = forms.ChoiceField(
        choices=INQUIRY_STATUS_CHOICES,
        required=False,
        label="작업 요청 상태"
    )

    class Meta:
        model = Task
        fields = ["inquiry", "inquiry_status", "ship_name", "block_name", "description", "manager", "work_date", "work_time",]
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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields["inquiry"].widget = forms.Select(
            choices=[(obj.id, f"{obj.ship_name} - {obj.block_name}") for obj in Inquiry.objects.all()]
        )
        
        # 작업 요청 필드의 선택 옵션을 ship_name - block_name 형식으로 표시
        self.fields["inquiry"].label_from_instance = (
            lambda obj: f"{obj.ship_name} - {obj.block_name}"
        )

        # 담당자 필드의 선택 옵션을 username으로 표시
        self.fields["manager"].label_from_instance = lambda obj: obj.name
        
        # 현재 로그인한 사용자를 담당자 필드의 초기값으로 설정
        if self.user and self.user.is_authenticated:
            self.initial['manager'] = self.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('inquiry_status'):
            instance.inquiry.status = self.cleaned_data['inquiry_status']
            instance.inquiry.save()
        if commit:
            instance.save()
        return instance

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task, Inquiry
from .forms import TaskForm
import calendar
from datetime import datetime, date, timedelta
from django.db.models import Q
from django.template import Library
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from users.models import User
from django.http import FileResponse
register = Library()


@register.filter
def filter_work_time(tasks, time_slot):
    return tasks.filter(work_time=time_slot)


# Create your views here.
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save()
            # 작업이 inquiry와 연결되어 있고, inquiry가 있는 경우 status를 승인으로 변경
            if task.inquiry:
                task.inquiry.status = "승인"
                task.inquiry.save()
            return redirect("task_list")
    return render(request, "task_create.html", {"form": TaskForm(user=request.user)})


def task_create_internal(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    return render(request, "task_create_internal.html", {"form": TaskForm(user=request.user)})

def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    return render(request, "task_update.html", {"form": TaskForm(instance=task)})


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


@staff_member_required
def task_list(request):
    # 달력 데이터 처리
    d = get_date(request.GET.get("month", None))
    cal = calendar.Calendar()
    month_days = cal.monthdatescalendar(d.year, d.month)

    # 각 날짜별 작업 가져오기
    tasks = Task.objects.filter(Q(work_date__year=d.year, work_date__month=d.month))
    managers = User.objects.filter(is_staff=True)
    # 달력 데이터 구성
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            day_tasks = tasks.filter(work_date=day)
            week_data.append(
                {
                    "date": day,
                    "tasks": day_tasks,
                    "is_current_month": day.month == d.month,
                }
            )
        calendar_data.append(week_data)

    # 모든 작업 목록
    all_tasks = Task.objects.all()
    all_inquiry = Inquiry.objects.all()

    context = {
        "tasks": all_tasks,
        "calendar": calendar_data,
        "prev_month": prev_month(d),
        "next_month": next_month(d),
        "current_month": d.strftime("%Y년 %m월"),
        "managers": managers,
        "inquiry": all_inquiry,
        "form": TaskForm(user=request.user),
    }

    
    return render(request, "task_list.html", context)


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "task_detail.html", {"task": task})


def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect("task_list")


@csrf_exempt
def create_task_inline(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task.objects.create(
                ship_name=data.get('ship_name'),
                block_name=data.get('block_name'),
                description=data.get('description'),
                manager_id=data.get('manager'),
                work_date=data.get('work_date'),
                work_time=data.get('work_time')
            )
            return JsonResponse({'success': True, 'task_id': task.id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def reject_inquiry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inquiry_id = data.get('inquiry_id')
            rejection_reason = data.get('rejection_reason')
            
            if not rejection_reason:
                return JsonResponse({'success': False, 'message': '반려 사유를 입력해주세요.'})
                
            inquiry = Inquiry.objects.get(id=inquiry_id)
            inquiry.status = "반려"
            inquiry.rejection_reason = rejection_reason
            inquiry.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def update_task_field(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field = data.get('field')
            value = data.get('value')
            
            task = Task.objects.get(pk=pk)
            
            # 필드 업데이트
            if field == 'manager':
                task.manager_id = value
            elif field == 'work_date':
                task.work_date = value
            elif field == 'work_time':
                # work_time 형식 검증 (예: "오전 2시", "오후 3시")
                import re
                time_pattern = r'^(오전|오후)\s\d{1,2}시$'
                if re.match(time_pattern, value):
                    task.work_time = value
                else:
                    return JsonResponse({'success': False, 'message': '유효하지 않은 시간 형식입니다. (예: 오전 2시, 오후 3시)'})
            elif field == 'description':
                task.description = value
            elif field == 'ship_name':
                task.ship_name = value
            elif field == 'block_name':
                task.block_name = value
            elif field == 'inquiry_ship_name':
                if task.inquiry:
                    task.inquiry.ship_name = value
                    task.inquiry.save()
                else:
                    return JsonResponse({'success': False, 'message': '요청 작업이 아닙니다.'})
            elif field == 'inquiry_block_name':
                if task.inquiry:
                    task.inquiry.block_name = value
                    task.inquiry.save()
                else:
                    return JsonResponse({'success': False, 'message': '요청 작업이 아닙니다.'})
                
            task.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def upload_report(request, pk):
    if request.method == 'POST':
        try:
            task = Task.objects.get(pk=pk)
            if 'report_file' in request.FILES:
                task.report_file = request.FILES['report_file']
                if task.inquiry:  # inquiry가 있는 경우에만 status 업데이트
                    task.inquiry.status = "완료"
                    task.inquiry.save()
                task.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '파일이 없습니다.'})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': '작업을 찾을 수 없습니다.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


def download_report(request, pk):
    task = Task.objects.get(pk=pk)
    if task.report_file:
        response = FileResponse(task.report_file)
        response['Content-Disposition'] = f'attachment; filename="{task.report_file.name}"'
        return response
    else:
        return JsonResponse({'success': False, 'error': '리포트 파일이 없습니다.'})
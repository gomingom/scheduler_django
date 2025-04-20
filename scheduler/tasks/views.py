from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
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
register = Library()


@register.filter
def filter_work_time(tasks, time_slot):
    return tasks.filter(work_time=time_slot)


# Create your views here.
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
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

    context = {
        "tasks": all_tasks,
        "calendar": calendar_data,
        "prev_month": prev_month(d),
        "next_month": next_month(d),
        "current_month": d.strftime("%Y년 %m월"),
        "managers": managers,
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

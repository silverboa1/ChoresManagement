from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    login_url = "/accounts/login/"

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:list")
    template_name = "tasks/task_form.html"

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:list")
    template_name = "tasks/task_form.html"

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

from django.http import JsonResponse

def update_task_status(request, pk):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            task = Task.objects.get(pk=pk)
            if status in dict(Task.STATUS_CHOICES).keys():
                task.status = status
                task.save()
                return JsonResponse({"success": True, "status_display": task.get_status_display()})
            else:
                return JsonResponse({"success": False, "error": "Невірний статус"})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})
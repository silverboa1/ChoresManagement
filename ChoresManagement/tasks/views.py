from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from django.shortcuts import redirect
from django.utils import timezone

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from .mixins import TaskOwnerMixin 

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)
    

class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:tasks_list")
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:tasks_list")

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:tasks_list")

def task_complete(request, pk):
    task = Task.objects.get(pk = pk)
    task.status = "completed"
    task.completed_at = timezone.now()
    task.progress = 100
    task.save()
    return redirect("tasks:task_list")
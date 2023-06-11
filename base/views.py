from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from django.views.decorators.csrf import csrf_protect
@csrf_protect
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)  # this will login the user
        return super(RegisterPage, self).form_valid(form)  # this will redirect to the success url

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:  # if user is already logged in then it will redirect to the task list page
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)  # this will redirect to the success url


class TaskList(LoginRequiredMixin,
               ListView):  # if user is not logged in then it will redirect to the login page(we need to add LOGIN_URL in settings.py
    # default template name is task_list.html
    model = Task
    context_object_name = 'tasks'  # this will change the name of the object from task_list to tasks

    def get_context_data(self, **kwargs):  # this will filter the tasks by user
        context = super().get_context_data(**kwargs)  # this will get the context data from the parent class
        context['tasks'] = context['tasks'].filter(user=self.request.user)  # this will filter the tasks by user
        context['count'] = context['tasks'].filter(
            complete=False).count()  # this will count the number of incomplete tasks

        search_input = self.request.GET.get('search-area') or ''  # this will get the search input from the search box
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)  # this will filter the tasks by title

        context['search_input'] = search_input  # this will pass the search input to the template

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'  # this will change the name of the object from task to task
    template_name = 'base/task.html'  # this will change the name of the template from task_detail to task


class TaskCreate(LoginRequiredMixin, CreateView):
    # default template name is task_form.html
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')  # this will redirect to the task list page after creating a new task

    def form_valid(self, form):  # this will set the user field to the current user
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    # default template name is task_form.html
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')  # this will redirect to the task list page after creating a new task


class DeleteView(DeleteView):
    # default template name is task_confirm_delete.html
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')  # this will redirect to the task list page after creating a new task
    template_name = 'base/delete.html'  # this will change the name of the template from task_confirm_delete to delete


def TaskComplete(request, pk):
    task = Task.objects.get(id=pk)
    task.complete = True
    task.save()
    return redirect('tasks')

def TaskUncomplete(request, pk):
    task = Task.objects.get(id=pk)
    task.complete = False
    task.save()
    return redirect('tasks')

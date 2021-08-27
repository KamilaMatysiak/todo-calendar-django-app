from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import datetime


# Create your views here.

def homepage(request):
    """
    Show homepage
    Args:
        request: request to return .html file

    Returns: .html file of homepage.

    """
    return render(request, 'tasks/index.html')


@login_required
def task_list(request):
    """
    Shows all tasks of specific user
    Args:
        request: request to return .html file

    Returns: .html of all tasks.

    """
    tasks = (x for x in Task.objects.all() if x.user == request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"tasks": tasks, 'form': form}
    return render(request, 'tasks/task-list.html', context)


def index(request):
    """
    Show homepage
    Args:
        request: request to return .html file

    Returns: .html file of homepage.

    """
    return render(request, 'tasks/vtodo.html')


def addTask(request):
    """
    Adds new task to list of tasks
    Args:
        request: request to return .html file

    Returns: .html file of add-task.

    """
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.user = request.user
            instance.save()
        return redirect('list')

    context = {"tasks": tasks, 'form': form}
    return render(request, 'tasks/add_task.html', context)


def updateTask(request, pk):
    """
    Lets user update their task.
    Args:
        request: request to return .html file

    Returns: .html file of update-task

    """
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list')

    context = {'form': form, 'id': pk}

    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    """
    Lets user delete task
    Args:
        request: request to return .html file

    Returns: .html file of delete-task.

    """
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list')

    context = {'item': item, 'id': pk}
    return render(request, 'tasks/delet.html', context)

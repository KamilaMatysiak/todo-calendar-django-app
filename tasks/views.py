from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import datetime
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView


# Create your views here.

def homepage(request):
    """
    Show homepage
    Args:
        request: request to return .html file

    Returns: .html file of homepage.

    """
    return render(request, 'tasks/index.html')

def test(request):
    return render(request, 'tasks/components.html')
    
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
    return render(request, 'tasks/vtodo.html')


class AddTaskView(BSModalCreateView):
    template_name = 'tasks/add_task.html'
    form_class = TaskModelForm
    success_message = "Dodano zadanie"
    success_url = reverse_lazy('list')
    
    
class EditTaskView(BSModalUpdateView):
    model = Task
    template_name = 'tasks/update_task.html'
    form_class = TaskModelForm
    success_message = "Pomyślnie zedytowano zadanie"
    success_url = reverse_lazy('list')


class DeleteTaskView(BSModalDeleteView):
    template_name = 'tasks/delet.html'
    model = Task
    success_message = "Pomyślnie usunięto zadanie"
    success_url = reverse_lazy('list')



   
  #  def get_object(self):
#        id_ = self.kwargs.get("id")
#        return get_object_or_404(Task, id=id_)

#def addTask(request):
  #  tasks = Task.objects.all()
 #   form = TaskForm()

#    if request.method == 'POST':
       # form = TaskForm(request.POST)
      #  if form.is_valid():
       #     form.save()
     #   return redirect('list')

    #context = {"tasks": tasks, 'form': form}
    #return render(request, 'tasks/add_task.html', #context)


def updateTask(request, pk):
    """
    Lets user update their task.
    Args:
        request: request to return .html file

    Returns: .html file of update-task

    """
    task = Task.objects.get(id=pk)
    form = TaskModelForm(instance=task)

    if request.method == 'POST':
        form = TaskModelForm(request.POST, instance=task)
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

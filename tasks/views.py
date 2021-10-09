from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import datetime
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic
import folium


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
    tasks = [x for x in Task.objects.all() if x.user == request.user]
    categories = [x for x in Category.objects.all() if x.user == request.user]
    #tasks = Task.objects.all()
    form = TaskModelForm()

    if request.method == 'POST':
        form = TaskModelForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"categories": categories, "tasks": tasks, 'form': form}
    return render(request, 'tasks/task-list.html', context)

def categoryView(request, title):
    category = Category.objects.get(title=title)
    categories = [x for x in Category.objects.all() if x.user == request.user]
    tasks = [x for x in Task.objects.all() if x.user == request.user and x.category is not None and x.category.title == category.title]

    form = TaskModelForm()

    if request.method == 'POST':
        form = TaskModelForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"categories": categories, "tasks": tasks, 'form': form, 'category': category}
    return render(request, 'tasks/category_template.html', context)

def index(request):
    return render(request, 'tasks/vtodo.html')


class AddTaskView(BSModalCreateView):
    template_name = 'tasks/add_task.html'
    form_class = TaskModelForm
    success_message = "Dodano zadanie"
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        if obj.localization:
            geolocator = Nominatim(user_agent='measurements')
            destination_ = form.cleaned_data.get('localization')
            destination = geolocator.geocode(destination_)
            obj.l_lat = destination.latitude
            obj.l_lon = destination.longitude
        return super(AddTaskView, self).form_valid(form)


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
            instance = form.save(commit=False)
            if instance.localization:
                geolocator = Nominatim(user_agent='measurements')
                destination_ = form.cleaned_data.get('localization')
                destination = geolocator.geocode(destination_)
                instance.l_lat = destination.latitude
                instance.l_lon = destination.longitude
            instance.save()
            return redirect('list')

    context = {'form': form, 'id': pk}

    return render(request, 'tasks/update_task.html', context)	


def finishTask(request):
    taskID = request.POST['taskID']
    complete = request.POST['complete']
    task = Task.objects.get(pk=taskID)

    if complete == 'true':
        print("saving to true")
        task.complete = True
    else:
        print("saving to false")
        task.complete = False

    task.save()
    return HttpResponse('')

class AddCategoryView(BSModalCreateView):
    template_name = 'tasks/add_category.html'
    form_class = CategoryModelForm
    success_message = "Dodano kategorię"
    success_url = reverse_lazy('list')

class EditCategoryView(BSModalUpdateView):
    model = Category
    template_name = 'tasks/update_category.html'
    form_class = TaskModelForm
    success_message = "Nazwa kategorii zmieniona pomyślnie"
    success_url = reverse_lazy('list')

class DeleteCategoryView(BSModalDeleteView):
    template_name = 'tasks/delete-category.html'
    model = Category
    success_message = "Pomyślnie usunięto zadanie"
    success_url = reverse_lazy('list')
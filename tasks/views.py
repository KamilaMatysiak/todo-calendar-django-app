from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from .models import *
from .forms import *
from calendar_app.models import Meeting
from geolocation.views import *
from django.urls import reverse_lazy, reverse
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from webpush import send_user_notification
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic
from django.http import Http404
from django.conf.urls.static import static
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from dateutil import relativedelta
from django.template import loader
import datetime
import json
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

def homepage(request):
    return render(request, 'tasks/index.html')


def terms_of_service(request):
    return render(request, 'tasks/terms_of_service.html')

def user_manual(request):
    return render(request, 'tasks/manual/user_manual.html')

def pwa_manual(request):
    return render(request, 'tasks/manual/pwa_instruction.html')

def test(request):
    return render(request, 'tasks/components.html')



@login_required
def task_list(request, pk=None):
    tasks = [x for x in Task.objects.all() if x.user == request.user and x.accepted == True]
    tasks = []
    for x in Task.objects.all():
        if x.user == request.user and x.accepted == True:
            if x.complete:
                if (datetime.datetime.now(timezone.utc)-x.completed_date).days > 7:
                    continue
            tasks.append(x)
    categories = [x for x in Category.objects.all() if x.user == request.user]
    form = TaskModelForm(request.user)

    if request.method == 'POST':
        form = TaskModelForm(request.user, request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"categories": categories, "tasks": tasks, 'form': form, 'API_KEY': settings.GOOGLE_API_KEY}
    if pk is not None:
        context["task_pk"] = pk
    return render(request, 'tasks/task-list.html', context)


def categoryView(request, pk):
    category = Category.objects.get(id=pk)
    categories = [x for x in Category.objects.all() if x.user == request.user]
    tasks = []
    for x in Task.objects.all():
        if x.user == request.user and x.category is not None and x.category.id == category.id and x.accepted == True:
            if x.complete:
                if (datetime.datetime.now(timezone.utc)-x.completed_date).days > 7:
                    continue
            tasks.append(x)

    form = TaskModelForm(request.user)

    if request.method == 'POST':
        form = TaskModelForm(request.user, request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"categories": categories, "tasks": tasks, 'form': form, 'category': category}
    return render(request, 'tasks/category_template.html', context)

def archiveView(request):
    categories = [x for x in Category.objects.all() if x.user == request.user]
    tasks = []
    for x in Task.objects.all():
        if x.user == request.user and x.accepted == True and x.completed_date:
            if (datetime.datetime.now(timezone.utc)-x.completed_date).days > 7:
                tasks.append(x)

    form = TaskModelForm(request.user)

    if request.method == 'POST':
        form = TaskModelForm(request.user, request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"categories": categories, "tasks": tasks, 'form': form}
    return render(request, 'tasks/archive.html', context)

def delegateView(request):
    categories = [x for x in Category.objects.all() if x.user == request.user]
    tasks = [x for x in Task.objects.all() if x.from_who is not None and x.from_who == request.user]
    form = TaskModelForm(request.user)

    if request.method == 'POST':
        form = TaskModelForm(request.user, request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')

    context = {"categories": categories, "tasks": tasks, 'form': form}
    return render(request, 'tasks/delegate.html', context)

@require_POST
@csrf_exempt
def send_push(request):
    user = request.user
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print(is_ajax)
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            lat = data.get('lat')
            lon = data.get('lon')
            return send_push_inner(request, user, (lat, lon), (data.get("oldLat"), data.get("oldLon")))
    return None

def index(request):
    count = 0
    today = []
    today_events = []
    priority = []
    here = []
    late = []

    events = [x for x in Meeting.objects.all() if x.user == request.user]
    not_accepted_tasks = [x for x in Task.objects.all() if x.user == request.user and x.accepted == False]
    for x in events:
        if x.date_start == datetime.date.today() and x.time_end > datetime.datetime.now().time():
            today_events.append(x)

    tasks = [x for x in Task.objects.all() if x.user == request.user and x.accepted == True]
    for x in tasks:
        if not x.complete:
            if x.date == datetime.date.today():
                count = count + 1
                today.append(x)
                if not x.complete and x.time < datetime.datetime.now().time():
                    late.append(x)
            if x.priority == "H":
                priority.append(x)

    context = {"tasks": tasks,
               "today": today,
               "high": priority,
               "late": late,
               "here": here,
               "events": today_events[:5],
               "user": request.user,
               "to_accept": not_accepted_tasks}
    return render(request, 'tasks/vtodo.html', context)


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
        with_who = self.request.POST.getlist("with_who")
        obj.with_who = "|".join(with_who)
        if not form.cleaned_data['is_cyclical']:
            obj.cycle_interval = None
            obj.cycle_number = None
        print(obj.cycle_interval)
        if form.cleaned_data.get('for_who') != "":
            for x in User.objects.all():
                if x.username == form.cleaned_data.get('for_who'):
                    obj.from_who = self.request.user
                    id = x.id
                    print(id)
                    obj.user = User.objects.get(id=id)
                    obj.accepted = False
                    return super(AddTaskView, self).form_valid(form)
            return Http404


        return super(AddTaskView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddTaskView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditTaskView(BSModalUpdateView):
    model = Task
    template_name = 'tasks/update_task.html'
    form_class = TaskModelForm
    success_message = "Pomyślnie zedytowano zadanie"
    success_url = reverse_lazy('list')

    @xframe_options_exempt
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        if obj.localization:
            geolocator = Nominatim(user_agent='measurements')
            destination_ = form.cleaned_data.get('localization')
            destination = geolocator.geocode(destination_)
            obj.l_lat = destination.latitude
            obj.l_lon = destination.longitude
        with_who = self.request.POST.getlist("with_who")
        obj.with_who = "|".join(with_who)
        return super(EditTaskView, self).form_valid(form)

    def get_object(self, queryset=None):
        obj = super(EditTaskView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_form_kwargs(self):
        kwargs = super(EditTaskView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        return context

class DeleteTaskView(BSModalDeleteView):
    template_name = 'tasks/delet.html'
    model = Task
    success_message = "Pomyślnie usunięto zadanie"
    success_url = reverse_lazy('list')

    def get_object(self, queryset=None):
        obj = super(DeleteTaskView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


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

def add_days(date, interval, number):
    if interval == 'd':
        d = datetime.timedelta(days = number)
    elif interval == 'w':
        d = datetime.timedelta(weeks = number)
    elif interval == 'm':
        d = relativedelta.relativedelta(months = number)
    elif interval == 'y':
        d = relativedelta.relativedelta(years = number)
    date += d
    return(date)

def finishTask(request):
    taskID = request.POST['taskID']
    complete = request.POST['complete']
    task = Task.objects.get(pk=taskID)

    if complete == 'true':
        task.complete = True
        task.completed_date = datetime.datetime.now(timezone.utc)
        print(task.completed_date)
        if task.is_cyclical:
            d = task.date
            while datetime.datetime.combine(d, task.time) < datetime.datetime.now():
                d = add_days(d, task.cycle_interval, task.cycle_number)
            if d == task.date:
                d = add_days(d, task.cycle_interval, task.cycle_number)
            Task.objects.create(user = task.user, title = task.title,
                localization = task.localization, with_who = task.with_who, date = d,
                time = task.time, priority = task.priority, category = task.category,
                is_cyclical = task.is_cyclical, cycle_interval = task.cycle_interval, cycle_number = task.cycle_number,
                complete = False, created = datetime.datetime.now(),
                from_who = task.from_who, accepted = True, meeting = task.meeting)
    else:
        print("saving to false")
        task.complete = False

    task.save()
    return HttpResponse('')


def send_push_inner(request, user, new, old):
    lat, lon = new
    oldLat, oldLon = old

    print(f"lat {lat} lon {lon} oldLat {oldLat} oldLon {oldLon}")
    try:
        old_data_task = is_any_task_close(user, oldLat, oldLon)
        data_task = is_any_task_close(user, lat, lon)
        print("old_data_task", old_data_task)
        print("data_task", data_task)
        if data_task is not None and old_data_task != data_task:
            payload = {'head': 'Masz zadanie w okolicy!',
                       'body': data_task}
            print(payload)
            send_user_notification(user=user, payload=payload, ttl=1000)
            return JsonResponse(status=200, data={"message": "Web push successful"})
        return JsonResponse(status=200, data={"message": "Nothing happened"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})


class AddCategoryView(BSModalCreateView):
    template_name = 'tasks/add_category.html'
    form_class = CategoryModelForm
    success_message = "Dodano kategorię"
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(AddCategoryView, self).form_valid(form)


class EditCategoryView(BSModalUpdateView):
    model = Category
    template_name = 'tasks/edit_cat.html'
    form_class = CategoryModelForm
    success_message = "Nazwa kategorii zmieniona pomyślnie"
    success_url = reverse_lazy('list')

    def get_object(self, queryset=None):
        obj = super(EditCategoryView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class DeleteCategoryView(BSModalDeleteView):
    template_name = 'tasks/delete-category.html'
    model = Category
    success_message = "Pomyślnie usunięto zadanie"
    success_url = reverse_lazy('list')

    def get_object(self, queryset=None):
        obj = super(DeleteCategoryView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


def refuse_task(request, pk):
    obj = get_object_or_404(Task, pk=pk)  # Get your current cat

    if request.method == 'POST':  # If method is POST,
        obj.delete()  # delete the cat.
    return redirect('vtodo')  # Finally, redirect to the homepage.


def accept_task(request, pk):
    obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        obj.accepted = True
        obj.save()
    return redirect('vtodo')

def is_any_task_close(user, lat, lon):
    nearest_task = None
    for x in Task.objects.all():
        if x.user == user and x.l_lat and x.l_lon:
            distance = geodesic((lat, lon), (x.l_lat, x.l_lon)).km
            if distance <= 5:
                nearest_task = x.title
                return (nearest_task)
    else:
        return None
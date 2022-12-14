import operator
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
import pytz
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

def error_404(request, exception):
    return render(request, 'offline.html')

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


@login_required
def index(request):
    count = 0
    today = []
    today_events = []
    priority = []
    here = []
    late = []
    notifications = []

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
    try:
        Notification.objects.all().delete
    except:
        print('huh')
    Notification.objects.filter(created__gte=(datetime.datetime.now(timezone.utc)-datetime.timedelta(days=7))).delete
    for x in Meeting.objects.all():
        if x.user == request.user and not Notification.objects.filter(user=request.user, meeting = x).exists() and (datetime.datetime.now()-datetime.timedelta(days=7)) < datetime.datetime.combine(x.date_end, x.time_end) <= datetime.datetime.now():
            Notification.objects.create(created = pytz.utc.localize(datetime.datetime.combine(x.date_end, x.time_end)), meeting = x, user = request.user)
        if x.user == request.user and x.is_cyclical:
            d = x.date_end
            while datetime.datetime.combine(d, x.time_end) <= datetime.datetime.now():
                if (datetime.datetime.now()-datetime.timedelta(days=7)) < datetime.datetime.combine(d, x.time_end) and not Notification.objects.filter(user=request.user, meeting=x, created=datetime.datetime.combine(d, x.time_end)).exists():
                    Notification.objects.create(created = pytz.utc.localize(datetime.datetime.combine(d, x.time_end)), meeting = x, user = request.user)
                d = add_days(d, x.cycle_interval, x.cycle_number)
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    notifications = [x for x in Notification.objects.filter(user=request.user, is_deleted=False)]
    notifications = sorted(notifications, key=operator.attrgetter('created'))

    context = {"tasks": tasks,
               "today": today,
               "high": priority,
               "late": late,
               "here": here,
               "events": today_events[:5],
               "user": request.user,
               "to_accept": not_accepted_tasks,
               'vapid_key': vapid_key,
               "notifications": notifications}
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
        if obj.is_cyclical and obj.cycle_number == None:
            obj.cycle_number = 1
        obj.with_who = "|".join(with_who)
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
    success_message = "Pomy??lnie zedytowano zadanie"
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
        if not obj.is_cyclical:
                obj.cycle_interval = 'd'
                obj.cycle_number = 1
        print('cycle number')
        print(obj.cycle_number)
        if obj.is_cyclical and obj.cycle_number == None:
            obj.cycle_number = 1
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
    success_message = "Pomy??lnie usuni??to zadanie"
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

@csrf_exempt
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

@require_POST
@csrf_exempt
def send_push(request):
    try:
        user = request.user
        body = request.body
        data = json.loads(body)
        #return send_push_inner(request, user, (lat, lon), (data.get("oldLat"), data.get("oldLon")))
        lat = data['lat'] 
        lon = data['lon']
        oldLat = data['oldLat'] 
        oldLon = data['oldLon']
        print(f"lat {lat} lon {lon} oldLat {oldLat} oldLon {oldLon}")
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

def is_any_task_close(user, lat, lon):
    nearest_task = None
    for x in Task.objects.all():
        if x.user == user and x.l_lat and x.l_lon:
            print('duh')
            distance = geodesic((lat, lon), (x.l_lat, x.l_lon)).km
            if distance <= 5:
                nearest_task = x.title
                return (nearest_task)
    else:
        return None

class AddCategoryView(BSModalCreateView):
    template_name = 'tasks/add_category.html'
    form_class = CategoryModelForm
    success_message = "Dodano kategori??"
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(AddCategoryView, self).form_valid(form)


class EditCategoryView(BSModalUpdateView):
    model = Category
    template_name = 'tasks/edit_cat.html'
    form_class = CategoryModelForm
    success_message = "Nazwa kategorii zmieniona pomy??lnie"
    success_url = reverse_lazy('list')

    def get_object(self, queryset=None):
        obj = super(EditCategoryView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class DeleteCategoryView(BSModalDeleteView):
    template_name = 'tasks/delete-category.html'
    model = Category
    success_message = "Pomy??lnie usuni??to zadanie"
    success_url = reverse_lazy('list')

    def get_object(self, queryset=None):
        obj = super(DeleteCategoryView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


def refuse_task(request, pk):
    obj = get_object_or_404(Task, pk=pk)  # Get your current cat

    if request.method == 'POST':  # If method is POST,
        obj.delete()
    return redirect('vtodo')  # Finally, redirect to the homepage.

def accept_task(request, pk):
    obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        obj.accepted = True
        obj.save()
    return redirect('vtodo')


def reject_notification(request, pk):
    obj = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':  # If method is POST,
        obj.is_deleted = True
        obj.save()
    return redirect('vtodo')

def accept_notification(request, pk):
    obj = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':  # If method is POST,
        obj.is_deleted = True
        obj.save()
    return redirect('list')
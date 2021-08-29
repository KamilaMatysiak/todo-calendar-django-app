from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from geopy.distance import geodesic
import folium


def location(request):
    """Shows a map with starting point of user, based on users localization.
        If user provide name of location,
         then map will show both starting point and destination with a line connecting  them

    Args:
        request: request to return .html file
    Returns:
        .html file with a map of user starting point and places with task assigned to them

    """

    distance = None
    destination = None

    #nie odkomentowuj bo on psuje wszystko
    #obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')
    ip_ = get_ip_address(request)
    print(ip_)
    ip = '109.173.220.158'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # koordynanty
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # inicjowanie mapy
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
    # znacznik lokalizacji początkowej
    folium.Marker([l_lat, l_lon], tooltip='twoja lokalizacja',
                  popup="kod pocztowy: " + city['postal_code'] + " miasto: " + city['city'],
                  icon=folium.Icon('green')).add_to(m)
    # Jeżeli  uzytkownik poda prawidłową lokalizację, pokaż miejsce startowe i docelowe
    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # koordynanty celu
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        # obliczanie odległości
        distance = round(geodesic(pointA, pointB).km, 2)

        # zainicjowanie mapy
        m = folium.Map(width=800, height=500,
                       location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
                       zoom_start=get_zoom(distance))
        #  znacznik lokacji początkowej
        folium.Marker([l_lat, l_lon], tooltip='twoja lokalizacja',
                      popup="kod pocztowy: " + city['postal_code'] + " miasto: " + city['city'],
                      icon=folium.Icon('green')).add_to(m)

        # znacznik lokacji celu
        folium.Marker([d_lat, d_lon], tooltip='cel podróży',
                      popup=destination,
                      icon=folium.Icon('red', icon="cloud")).add_to(m)

        # linia pomiędzy punktem początkowym i docelowym
        line = folium.PolyLine(locations=[pointA, pointB], weight=2, color='blue')
        m.add_child(line)

        # modyfikacja mapy
        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()
    distance = None

    context = {
        'distance': distance,
        'destination': destination,
        'form': form,
        'map': m,
    }

    return render(request, 'geolocation/location.html', context)

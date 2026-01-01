from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=e8d7d6f4fe92b6dd78e2415a5c765d00&units=metric'

   if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            NCity = form.cleaned_data['name']
            city_exists = City.objects.filter(name__iexact=NCity).exists()


            if city_exists == 0:
                res = requests.get(url.format(NCity))
                data = res.json()

                if data["cod"] == 200:
                    form.save()
                    messages.success(request, f"{NCity} added successfully!")
                else:
                    messages.error(request, "City does not exist!")
            else:
                messages.error(request, "City already exists!")
    else:
        form = CityForm()

    # Fetch weather for all cities
    cities = City.objects.all()
    data = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_weather = {
            'city': city.name,
            'temperature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'country': res['sys']['country'],
            'icon': res['weather'][0]['icon'],
        }
        data.append(city_weather)

    # context OUTSIDE loop
    context = {'data': data, 'form': form}
    return render(request, "weatherapp.html", context)


def delete_city(request, CName):
    deleted, _ = City.objects.filter(name__iexact=CName).delete()

    if deleted:
        messages.success(request, f"{CName} removed successfully!")
    else:
        messages.error(request, f"{CName} not found!")

    return redirect('home')


from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from collections import defaultdict
from datetime import datetime
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        messages.success(request, 'Success! Form submitted! Let’s get started👍')
        return redirect('weather')
    else:
        return render(request, 'login.html')



def about(request):
    return render(request, 'about.html')
def weather(request):
        if request.method == 'POST':
            city = request.POST['city']
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=your_openweathermap_api_key'
            city_weather = requests.get(url.format(city)).json()
            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
            }
            context = {'weather': weather}
            return render(request, 'weather_results.html', context)
        else:
            return render(request, 'weather.html')
def weather_results(request):
    if request.method == 'POST':
        city = request.POST['city']
        url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=97c2ab1de2d76cb84b1fda826720f7f9'
        city_weather = requests.get(url.format(city)).json()
        forecast_data = defaultdict(list)
        for item in city_weather['list']:
            date = item['dt_txt'].split(' ')[0]  # Only get the date part
            forecast_data[date].append(item)
        weather = {
            'city' : city,
            'temperature' : round(city_weather['list'][0]['main']['temp']),  # Round off the temperature
            'wind': city_weather['list'][0]['wind']['speed'],
            'precip': city_weather['list'][0]['rain']['3h'] if 'rain' in city_weather['list'][0] and '3h' in
                                                               city_weather['list'][0]['rain'] else 0,

            'pressure': city_weather['list'][0]['main']['pressure'],
            'description' : city_weather['list'][0]['weather'][0]['description'],
            'icon' : city_weather['list'][0]['weather'][0]['icon'],  # Ensure the icon is included
            'forecast': [
                {
                    'date': date,
                    'temperature': round(sum(item['main']['temp'] for item in items) / len(items)),  # Calculate average temperature and round off
                    'icon': items[0]['weather'][0]['icon'],  # Use the icon from the first forecast of the day
                }
                for date, items in sorted(forecast_data.items())[:7]  # Get the forecast for the next 7 days
            ],
        }
        context = {'weather' : weather}
        return render(request, 'weather_results.html', context)
    else:
        return render(request, 'weather.html')
def signup(request):
    return render(request, 'signup.html')
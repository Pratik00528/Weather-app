# Importing necessary libraries
from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime, timedelta
import calendar

# Initializing Flask application
app = Flask(__name__)

# Define custom Jinja filter
@app.template_filter('timestamp_to_local')
def timestamp_to_local(timestamp, timezone):
    user_timezone = pytz.timezone(pytz.all_timezones[timezone])
    local_time = datetime.fromtimestamp(timestamp, tz=pytz.utc).astimezone(user_timezone)
    return local_time.strftime('%H:%M:%S')

# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():

    data = None
    city = None

    cities = ['Delhi', 'London', 'New York', 'Paris', 'Dubai', 'Tokyo']
    city_data = {}


    if request.method == 'POST':

        city = request.form.get('city')

        data = get_weather(city)

    for city_name in cities: # For getting the weather information for all other popular cities
        city_data[city_name] = get_weather(city_name)

    return render_template('index.html', city = city, data = data, city_data = city_data)

def get_weather(city):

    try:

        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=d1ea9a4c24706d113d8590febab110aa')

        #read the json object
        json_object = r.json()

        sunrise_time = int(json_object['sys']['sunrise'])
        sunset_time = int(json_object['sys']['sunset'])

        timezone = int(json_object['timezone'])

        # Convert Unix time to datetime object
        sunrise_time = datetime.utcfromtimestamp(sunrise_time)
        sunset_time = datetime.utcfromtimestamp(sunset_time)

        # Calculate the timezone offset as a timedelta
        offset = timedelta(seconds = timezone)
        
        # Get the current UTC time
        current_time_utc = datetime.utcnow()

        # Convert the UTC time to the city's local time
        local_time = current_time_utc + offset

       # Get the day number, month name, and day name
        day_number = local_time.day
        month_name = calendar.month_name[local_time.month]
        day_name = local_time.strftime('%A')

        # Placeholder data (replace with actual data)
        weather_data = {
            'temperature' : int(json_object['main']['temp'] - 273.15),
            'min_temp' : int(json_object['main']['temp_min'] - 273.15),
            'max_temp' : int(json_object['main']['temp_max'] - 273.15),
            'humidity' : int(json_object['main']['humidity']),
            'pressure' : int(json_object['main']['pressure']),
            'wind' : int(json_object['wind']['speed']),
            'description' : json_object['weather'][0]['description'],
            'condition' : json_object['weather'][0]['main'],
            'icon' : json_object['weather'][0]['icon'],
            'sunrise' : (sunrise_time + offset).strftime('%H:%M:%S'),
            'sunset' : (sunset_time + offset).strftime('%H:%M:%S'),
            'city_name' : json_object['name'],
            'country_code' : json_object['sys']['country'], 
            'time' : local_time.strftime('%I:%M %p'),
            'hour' : int(local_time.strftime('%H'))

                        }

        # Update the weather_data dictionary to include day_number, month_name, and day_name
        weather_data['day_number'] = day_number
        weather_data['month_name'] = month_name
        weather_data['day_name'] = day_name

        return weather_data

    except KeyError:

        return "Enter a valid city name!"

    except:
        return "Sorry something went wrong."

@app.route('/about')
def about():

    try:
        return render_template('about.html')
    
    except:
        return "Sorry something went wrong."

@app.route('/how_to_use')
def how_to_use():

    try:
        return render_template('how_to_use.html')
    
    except:
        return "Sorry something went wrong."


# Running the application
if __name__ == '__main__':
    app.run(debug=True)





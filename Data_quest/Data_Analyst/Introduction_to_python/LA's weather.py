"""
In this mission, we'll be looking at weather data from Los Angeles (LA). This data is for each day in 2014, and tells us
the type of weather that LA experienced that day.
"""

"""
    Slice
"""

weather_data = []

file = open("la_weather.csv","r")
data = file.read()
weather_data = [ i.split(',') for i in data.split("\n")]

#weather  contain each value from the Type of Weather column
weather = [i[1] for i in weather_data]

count = len(weather)

#remove the header
new_weather  = weather[1:]

#weather type
weather_types = ["Rain", "Sunny", "Fog", "Fog-Rain", "Thunderstorm", "Type of Weather"]
weather_type_found = [ i in new_weather for i in weather_types]

"""
    dictionary
"""
# dictionnary of weather:count_weather
weather_counts = {j : len([i for i in weather if i == j]) for j in weather}


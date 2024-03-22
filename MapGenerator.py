import requests
from dotenv import load_dotenv
import os
import folium
import webbrowser

load_dotenv(".env")

# FETCH Latitude and Longitude based on location name
def fetchGeocode(accident_loc):
    url = "https://trueway-geocoding.p.rapidapi.com/Geocode"

    querystring = {"address":accident_loc,"language":"en"}

    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    d = response.json()["results"][0]["location"]

    return (d["lat"], d["lng"])

# FETCH name of closest establishment
def fetchClosestEstablishment(lat_lng, establishment):
    url = "https://maps-data.p.rapidapi.com/searchmaps.php"

    querystring = {"query":establishment,"limit":"20","country":"sg","lang":"en","lat":lat_lng[0],"lng":lat_lng[1],"offset":"0","zoom":"13"}

    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "maps-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    d = response.json()["data"][0]["name"]
    return d

# GETS the closest establishments in proximity to the accident location
# *establishments is optional, with minimum entry of 1
# under *establishments, you can input whatever you want. Eg: "Hospital", "Police Station", etc.
def getDesiredEstablishments(accident_loc, *establishments):
    tup = fetchGeocode(accident_loc)
    d = {}
    for i in establishments:
        name = fetchClosestEstablishment(tup, i)
        d[i] = name
    return d

# FINDS the best path between 2 locations, the accident, and the location
# return is in the form of many many coordinate nodes, stored as Pairs
def findBestPath(accident_loc, establishment_loc):

    url = "https://trueway-directions2.p.rapidapi.com/FindDrivingPath"
    
    accident_tup = fetchGeocode(accident_loc)
    establishment_tup = fetchGeocode(establishment_loc)

    querystring = {"origin":f'{accident_tup[0]}, {accident_tup[1]}',"destination":f'{establishment_tup[0]}, {establishment_tup[1]}'}

    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "trueway-directions2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()["route"]["geometry"]["coordinates"]

# RETURNS a map as a variable
def plotCoorsReturn(accident_loc, establishment_loc):
    coordinates = findBestPath(accident_loc, establishment_loc)
    
    # create map
    m = folium.Map(location=coordinates[0], zoom_start=12)
    
    # set pointer Start
    folium.Marker(
        coordinates[0],
        popup="Start",
        icon=folium.Icon(color='green')
    ).add_to(m)
    
    # set pointer End
    folium.Marker(
        coordinates[-1],
        popup='End',
        icon=folium.Icon(color='red')
    ).add_to(m)
    
    # set zoom scale. Add padding if you want to make it larger/smaller
    m.fit_bounds([coordinates[0], coordinates[-1]], padding=(150,150))
    
    # draw line
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)
    
    return m

# PLOTS for all establishments
def getAllPlots(accident_loc):
    establishment_d = getDesiredEstablishments(accident_loc, "Hospital", "Police Station", "Fire Station")
    plots = {}
    for establishment, closest in establishment_d.items():
        plots[establishment] = plotCoorsReturn(accident_loc, closest)
    return plots

# SAVE map as HTML
def plotCoorsHTML(accident_loc, establishment_loc):
    coordinates = findBestPath(accident_loc, establishment_loc)
    
    # create map
    m = folium.Map(location=coordinates[0], zoom_start=12)
    
    # set pointer Start
    folium.Marker(
        coordinates[0],
        popup="Start",
        icon=folium.Icon(color='green')
    ).add_to(m)
    
    # set pointer End
    folium.Marker(
        coordinates[-1],
        popup='End',
        icon=folium.Icon(color='red')
    ).add_to(m)
    
    # set zoom scale. Add padding if you want to make it larger/smaller
    m.fit_bounds([coordinates[0], coordinates[-1]], padding=(150,150))
    
    # draw line
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)
    
    m.save("map.html")

# PLOTS all establishments' routes based on location
def plotAllHTML(accident_loc):
    plots = getAllPlots(accident_loc)
    for establishment, plot in plots.items():
        html_saved = f"{establishment}.html"
        plot.save(html_saved)
        file_path = os.path.abspath(html_saved)
        webbrowser.open("file://" + file_path)
    
# for testing
# plotAllHTML("NUS")
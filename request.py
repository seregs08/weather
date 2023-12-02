import json

import requests

import config

def get_city_coord(city: str):
    payload = {'geocode' : city, 'apikey' : config.geo_key, 'format' : 'json'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo = json.loads(r.text)
    return geo['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
#get_city_coord('Краснодар')

def get_weather(city):
    coordinate = get_city_coord(city).split()
    payload = {'lat' : coordinate[1], 'lon' : coordinate[0], 'lang' : 'ru_RU'}
    r = requests.get('https://api.weather.yandex.ru/v2/forecast', params=payload, headers=config.weather_key)
    weather_data = json.loads(r.text)
    return print(weather_data['fact'])
get_weather('Краснодар')
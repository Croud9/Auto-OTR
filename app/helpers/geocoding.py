from time import sleep
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises", timeout = 1)

def get_full_address_by_coordinates(lat, long):
    coord = f"{lat}, {long}"
    geodata = {}
    sleep(1)
    full_address_name = geolocator.reverse(coord, exactly_one=True, language='ru')
    if not full_address_name:
        geodata['full_address'] = 'Неправильный формат координат (пример 11.22, 33.44)'
        return geodata
    address = full_address_name.raw['address']
    geodata['num_house'] = address.get('house_number', '')
    geodata['road'] = address.get('road', '')
    geodata['city'] = address.get('city', '')
    geodata['town'] = address.get('town', '')
    geodata['village'] = address.get('village', '')
    geodata['state'] = address.get('state', '')
    geodata['country'] = address.get('country', '')
    geodata['full_address'] = ", ".join([geodata['country'], geodata['state'], geodata['city'], geodata['town'], geodata['village'], geodata['road'], geodata['num_house']])
    if ' ,' in geodata['full_address']:
        geodata['full_address'] = geodata['full_address'].replace(' ,', '')
    
    if geodata['city'] != '':
        geodata['city_point'] = geodata['city']
    elif geodata['town'] != '':
        geodata['city_point'] = geodata['town']
    elif geodata['village'] != '':
        geodata['city_point'] = geodata['village']
    else:
        geodata['city_point'] = ''
        
    return geodata

def get_coordinates_by_full_address(adr):
    coord = {}
    sleep(1)
    coordinate_location = geolocator.geocode(adr)   
    if not coordinate_location:
        coord['error'] = 'Неправильный формат адреса (должен быть без сокращений )'
        return coord 
    coord ['latitude'] = coordinate_location.raw.get('lat', '')
    coord ['longitude'] = coordinate_location.raw.get('lon', '')
    geodata = get_full_address_by_coordinates(coord ['latitude'], coord ['longitude'])
    coord ['full_address'] = geodata['full_address']
    if geodata['city'] != '':
        coord ['city'] = geodata['city']
    elif geodata['town'] != '':
        coord ['city'] = geodata['town']
    elif geodata['village'] != '':
        coord ['city'] = geodata['village']
    else:
        coord ['city'] = ''
    return coord 

# coord = {'latitude': 55.587562, 'longitude': 37.908986}
# adr = {'address': 'Екатеринбург, Анатолия Мехренцева, 36'}
# print(get_full_address_by_coordinates(55.587562, 3.908986))
# sleep(1)
# print(get_coordinates_by_full_address('Екатеринбург, Анатолия Мехренцева, 36'))
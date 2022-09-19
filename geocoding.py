from audioop import add
from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="geoapiExercises")

def get_full_address_by_coordinates(lat, long):
    coord = f"{lat}, {long}"
    sleep(1)
    full_address_name = geolocator.reverse(coord, exactly_one=True, language='ru')
    if not full_address_name:
        # print('Неправильный формат координат: ', coord)
        full_address = 'Неправильный формат координат (пример 11.22, 33.44)'
        return full_address
    address = full_address_name.raw['address']
    print(full_address_name.raw)
    num_house = address.get('house_number', '')
    road = address.get('road', '')
    city = address.get('town', '')
    village = address.get('village', '')
    state = address.get('state', '')
    country = address.get('country', '')
    full_address = ", ".join([country, state, city, village, road, num_house])
    if ' ,' in full_address:
        full_address = full_address.replace(' ,', '')
    return full_address

def get_coordinates_by_full_address(adr):
    coord = {}
    sleep(1)
    coordinate_location = geolocator.geocode(adr)   
    if not coordinate_location:
        # print('Неправильный формат адреса: ', adr)
        coord['error'] = 'Неправильный формат адреса (должен быть без сокращений )'
        return coord 
    coord ['latitude'] = coordinate_location.raw.get('lat', '')
    coord ['longitude'] = coordinate_location.raw.get('lon', '')
    return coord 

# coord = {'latitude': 55.587562, 'longitude': 37.908986}
# adr = {'address': 'Екатеринбург, Анатолия Мехренцева, 36'}
# print(get_full_address_by_coordinates(55.587562, 3.908986))
# sleep(1)
# print(get_coordinates_by_full_address('Екатеринбург, Анатолия Мехренцева, 36'))
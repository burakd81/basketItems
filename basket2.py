from geopy.geocoders import Nominatim
import random


class Sepet:
    def __init__(self):
        self.items = []
        self.geoCodes = []
        self.adresses = []
        self.mapsLinks = []
        self.geolocator = Nominatim(user_agent="test")
        
        self.dicts = {
            "items": self.items,
            "geoCodes": self.geoCodes,
            "adresses": self.adresses,
            "mapsLinks": self.mapsLinks,
            "geolocator": self.geolocator
        }
        
    def add_item(self, item_info):
        self.items.append(item_info['item'])
        self.geoCodes.append(item_info['geoCode'])
        location = self.geolocator.reverse(item_info['location'])
        self.adresses.append(location.address)
        self.mapsLinks.append(item_info['mapsLink'])

    def get_sepets(self, items_per_basket=10):
        sepets = []
        basket_count = len(self.items) // items_per_basket + (len(self.items) % items_per_basket > 0)
        for i in range(basket_count):
            start_index = i * items_per_basket
            end_index = start_index + items_per_basket
            sepets.append({
                'name': f'sepet{i+1}',
                'items': self.items[start_index:end_index],
                'geoCodes': self.geoCodes[start_index:end_index],
                'adresses': self.adresses[start_index:end_index],
                'mapsLinks': self.mapsLinks[start_index:end_index]
            })
        return sepets



my_basket = Sepet()



for i in range(500):
    lat = random.uniform(41.1142669, 41.1232601) # Enlem aralığı 1km 0.00899322 
    lng = random.uniform(29.0163493, 29.0163501) # Boylam aralığı 1 km yaklaşık 0.00000898
    location = f"{lat}, {lng}"
    link = f"https://www.google.com/maps?q={lat},{lng}"
    item_info = {'item': f'item{i}', 'geoCode': f'geoCode{lat,lng}', 'location': location, 'mapsLink': f'mapsLink{link}'}
    
    my_basket.add_item(item_info)




baskets = my_basket.get_sepets(items_per_basket=10)

for basket in baskets:
    basket_dict = dict(zip(['name', 'items', 'geoCodes', 'adresses', 'mapsLinks'], [basket['name'], basket['items'], basket['geoCodes'], basket['adresses'], basket['mapsLinks']]))
    print(basket_dict)
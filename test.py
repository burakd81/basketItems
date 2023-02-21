import unittest
from geopy.geocoders import Nominatim
from unittest.mock import patch
import random
from basket import Sepet

class TestSepet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geolocator = Nominatim(user_agent="test")

    def setUp(self):
        self.my_basket = Sepet()

    def test_add_item(self):
        # Sepete tek bir öğe ekleme testi
        item_info = {'item': 'test_item', 'geoCode': 'test_geoCode', 'location': '41.123456, 29.012345', 'mapsLink': 'test_mapsLink'}
        self.my_basket.add_item(item_info)
        self.assertEqual(len(self.my_basket.items), 1)
        self.assertEqual(len(self.my_basket.geoCodes), 1)
        self.assertEqual(len(self.my_basket.adresses), 1)
        self.assertEqual(len(self.my_basket.mapsLinks), 1)

    def test_get_sepets(self):
        # Farklı sayıda ürünle sepet oluşturma testi 
        for i in range(5):
            for j in range(random.randint(1, 20)):
                lat = random.uniform(41.1142669, 41.1232601)
                lng = random.uniform(29.0163493, 29.0163501)
                location = f"{lat}, {lng}"
                link = f"https://www.google.com/maps?q={lat},{lng}"
                item_info = {'item': f'item{j}', 'geoCode': f'geoCode{lat,lng}', 'location': location, 'mapsLink': f'mapsLink{link}'}
                self.my_basket.add_item(item_info)

            sepets = self.my_basket.get_sepets(items_per_basket=i+1)
            self.assertEqual(len(sepets), len(self.my_basket.items) // (i+1) + (len(self.my_basket.items) % (i+1) > 0))
            for basket in sepets:
                self.assertEqual(len(basket['items']), i+1)

    @patch.object(Nominatim, 'reverse')
    def test_geolocation(self, mock_reverse):
        # Ters coğrafi konumun doğru konum dizesiyle çağrıldığını test etme (Arkadaş destekli yapıldı.)
        item_info = {'item': 'test_item', 'geoCode': 'test_geoCode', 'location': '41.123456, 29.012345', 'mapsLink': 'test_mapsLink'}
        self.my_basket.add_item(item_info)
        mock_reverse.return_value.address = 'test_address'
        self.my_basket.get_sepets(items_per_basket=1)
        mock_reverse.assert_called_with('41.123456, 29.012345')

if __name__ == '__main__':
    unittest.main()

import unittest
import xmltodict
from zillow import Place

class TestGetSearchResult(unittest.TestCase):

    def test_search_results(self):
        RAW_XML = ""
        with open('./testdata/place.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place()
        place.set_data(data)

        self.assertEqual("2100641621", place.zpid)
        self.assertEqual(1723665, place.zestiamte.amount)


    def test_zestimate(self):
        RAW_XML = ""
        with open('./testdata/get_zestimate.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place()
        place.set_data(data)

        self.assertEqual("2100641621", place.zpid)
        self.assertEqual(1723665, place.zestiamte.amount)
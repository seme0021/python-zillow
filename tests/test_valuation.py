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
        place.set_data(data.get('SearchResults:searchresults', None)['response']['results']['result'])

        self.assertEqual("2100641621", place.zpid)
        self.assertEqual(1723665, place.zestiamte.amount)

    def test_zestimate(self):
        RAW_XML = ""
        with open('./testdata/get_zestimate.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place()
        place.set_data(data.get('Zestimate:zestimate', None)['response'])

        self.assertEqual("2100641621", place.zpid)
        self.assertEqual(1723665, place.zestiamte.amount)

    def test_getcomps_principal(self):
        RAW_XML = ""
        with open('./testdata/get_comps.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place()
        place.set_data(data.get('Comps:comps')['response']['properties']['principal'])

        self.assertEqual("2100641621", place.zpid)

    def test_getcomps_comps(self):
        RAW_XML = ""
        with open('./testdata/get_comps.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)
        comps = data.get('Comps:comps')['response']['properties']['comparables']['comp']

        comp_places = []

        for datum in comps:
            place = Place()
            place.set_data(datum)
            comp_places.append(place)

        self.assertEqual(10, len(comp_places))

    def test_extended_data(self):
        RAW_XML = ""
        with open('./testdata/get_deep_search_results.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place(has_extended_data=True)
        place.set_data(data.get('SearchResults:searchresults', None)['response']['results']['result'])

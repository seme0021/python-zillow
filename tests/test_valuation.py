import unittest
import warnings

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
        self.assertEqual(1723665, place.zestimate.amount)

    def test_zestimate(self):
        RAW_XML = ""
        with open('./testdata/get_zestimate.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place()
        place.set_data(data.get('Zestimate:zestimate', None)['response'])

        self.assertEqual("2100641621", place.zpid)
        self.assertEqual(1723665, place.zestimate.amount)

    def test_zestiamte(self):
        """Test that the backward-compatible ``zestiamte`` works.

        This property should correctly return the ``zestimate``
        attribute and raise a DeprecationWarning about the changing
        name.

        """
        warnings.simplefilter('always', DeprecationWarning)

        with open('./testdata/get_zestimate.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        data = xmltodict.parse(RAW_XML)

        place = Place()
        place.set_data(data.get('Zestimate:zestimate', None)['response'])

        self.assertEqual(place.zestiamte, place.zestimate)

        with warnings.catch_warnings(record=True) as warning:
            place.zestiamte
            assert issubclass(warning[0].category, DeprecationWarning)

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

        assert place.get_dict() is not None

    def test_get_deep_comps(self):
        RAW_XML = ""
        with open('./testdata/get_deep_comps.xml', 'r') as f:
            RAW_XML = ''.join(f.readlines())

        xmltodict_data = xmltodict.parse(RAW_XML)

        # get the principal property data
        principal_place = Place()
        principal_data = xmltodict_data.get('Comps:comps')['response']['properties']['principal']

        assert principal_data is not None

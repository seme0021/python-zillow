from abc import abstractmethod
import warnings


class SourceData(classmethod):

    @abstractmethod
    def set_data(self, source_data):
        """
        @type source_data: dict
        """
        raise NotImplementedError()

    @abstractmethod
    def debug(self):
        for i in self.__dict__.keys():
            print ("%s: %s" % (i, self.__dict__[i]))

    @abstractmethod
    def get_dict(self):
        res = {}
        for i in self.__dict__.keys():
            res[i] = self.__dict__[i]
        return res

    @abstractmethod
    def set_values_from_dict(self, data_dict):
        """
        @type data_dict: dict
        """
        for i in self.__dict__.keys():
            if i in data_dict.keys():
                self.__dict__[i] = data_dict[i]


class Links(SourceData):
    def __init__(self, **kwargs):
        self.home_details = None
        self.graphs_and_data = None
        self.map_this_home = None
        self.comparables = None

    def set_data(self, source_data):
        """
        :source_data: Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['links']
        :return:
        """
        self.home_details = source_data['homedetails']
        try:
            self.graphs_and_data = source_data['graphsanddata']
        except:
            self.graphs_and_data = None
        self.map_this_home = source_data['mapthishome']
        self.comparables = source_data['comparables']

class FullAddress(SourceData):
    def __init__(self, **kwargs):
        self.street = None
        self.zipcode = None
        self.city = None
        self.state = None
        self.latitude = None
        self.longitude = None

    def set_data(self, source_data):
        """
        :source_data: Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['address']
        :return:
        """
        self.street = source_data['street']
        self.zipcode = source_data['zipcode']
        self.city = source_data['city']
        self.state = source_data['state']
        self.latitude = source_data['latitude']
        self.longitude = source_data['longitude']

class ZEstimateData(SourceData):
    def __init__(self, **kwargs):
        self.amount = None
        self.amount_currency = None
        self.amount_last_updated = None
        self.amount_change_30days = None
        self.valuation_range_low = None
        self.valuation_range_high = None

    def set_data(self, source_data):
        """
        :source_data: Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['zestimate']
        :return:
        """
        try:
            self.amount = int(source_data['amount']['#text'])
        except:
            self.amount = None
        self.amount_currency = source_data['amount']['@currency']
        self.amount_last_updated = source_data['last-updated']
        try:
            self.amount_change_30days = int(source_data['valueChange']['#text'])
        except:
            self.amount_change_30days = None
        try:
            self.valuation_range_low = int(source_data['valuationRange']['low']['#text'])
        except:
            self.valuation_range_low = None
        try:
            self.valuation_range_high = int(source_data['valuationRange']['high']['#text'])
        except:
            self.valuation_range_high = None

class LocalRealEstate(SourceData):
    def __init__(self):
        self.region_name = None
        self.region_id = None
        self.region_type = None
        self.overview_link = None
        self.fsbo_link = None
        self.sale_link = None
        self.zillow_home_value_index = None

    def set_data(self, source_data):
        """
        :source_data": Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['localRealEstate']
        :return:
        """
        self.region_name = source_data['region']['@name']
        self.region_id = source_data['region']['@id']
        self.region_type =  source_data['region']['@type']
        self.zillow_home_value_index = source_data.get('zindexValue', None)
        self.overview_link =  source_data['region']['links']['overview']
        self.fsbo_link =  source_data['region']['links']['forSaleByOwner']
        self.sale_link =  source_data['region']['links']['forSale']

class ExtendedData(SourceData):
    def __init__(self):
        self.fips_county = None
        self.usecode = None
        self.tax_assessment_year = None
        self.tax_assessment = None
        self.year_built = None
        self.lot_size_sqft = None
        self.finished_sqft = None
        self.bathrooms = None
        self.bedrooms = None
        self.last_sold_date = None
        self.last_sold_price = None
        self.complete = False

    def set_data(self, source_data):
        self.fips_county = source_data.get('FIPScounty', None)
        self.usecode = source_data['useCode']
        self.tax_assessment_year = source_data.get('taxAssessmentYear', None)
        self.tax_assessment = source_data.get('taxAssessment', None)
        self.year_built = source_data.get('yearBuilt', None)
        self.lot_size_sqft = source_data.get('lotSizeSqFt', None)
        self.finished_sqft = source_data.get('finishedSqFt', None)
        self.bathrooms = source_data.get('bathrooms', None)
        self.bedrooms = source_data.get('bedrooms', None)
        self.last_sold_date = source_data.get('lastSoldDate', None)
        price_element = source_data.get('lastSoldPrice', None)
        if price_element is not None:
            self.last_sold_price = price_element.get('#text', None)
        self.complete = True


class Place(SourceData):
    """
    A class representing a property and it's details
    """
    def __init__(self, has_extended_data=False):
        self.zpid = None
        self.links = Links()
        self.full_address = FullAddress()
        self.zestimate = ZEstimateData()
        self.local_realestate = LocalRealEstate()
        self.similarity_score = None
        self.extended_data = ExtendedData()
        self.has_extended_data = has_extended_data

    @property
    def zestiamte(self):
        """Backward-compatible typo property to prevent breaking changes."""
        warnings.warn(
            'The ``zestiamte`` attribute has been renamed to '
            '``zestimate`` and will be removed in a future release.',
            DeprecationWarning,
        )
        return self.zestimate


    def set_data(self, source_data):
        """
        :source_data": Data from data.get('SearchResults:searchresults', None)['response']['results']['result']
        :param source_data:
        :return:
        """

        self.zpid = source_data.get('zpid', None)
        self.similarity_score = source_data.get('@score', None)
        self.links.set_data(source_data['links'])
        self.full_address.set_data(source_data['address'])
        self.zestimate.set_data(source_data['zestimate'])
        self.local_realestate.set_data(source_data['localRealEstate'])
        if self.has_extended_data:
            self.extended_data.set_data(source_data)

    def get_dict(self):
        data = {
            'zpid': self.zpid,
            'similarity_score': self.similarity_score,
            'links': self.links.get_dict(),
            'full_address': self.full_address.get_dict(),
            'zestimate': self.zestimate.get_dict(),
            'local_realestate': self.local_realestate.get_dict(),
            'extended_data': self.extended_data.get_dict()
        }
        return data

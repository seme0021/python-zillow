from zillow import (__author__, ZillowError, Place)
import xmltodict

import requests
try:
  # python 3
  from urllib.parse import urlparse, urlunparse, urlencode
  from urllib.request import urlopen
  from urllib.request import __version__ as urllib_version
except ImportError:
  from urlparse import urlparse, urlunparse
  from urllib2 import urlopen
  from urllib import urlencode
  from urllib import __version__ as urllib_version


class ValuationApi(object):
    """
    A python interface into the Zillow API
    By default, the Api caches results for 1 minute.
    Example usage:
      To create an instance of the zillow.ValuationApi class:
        >>> import zillow
        >>> api = zillow.ValuationApi()


    All available methods include:
        >>> data = api.GetSearchResults("<your key here>", "<your address here>", "<your zip here>")
    """
    def __init__(self):
        self.base_url = "https://www.zillow.com/webservice"
        self._input_encoding = None
        self._request_headers=None
        self.__auth = None
        self._timeout = None

    def GetSearchResults(self, zws_id, address, citystatezip, retnzestimate=False):
        """
        The GetSearchResults API finds a property for a specified address.
        The content returned contains the address for the property or properties as well as the Zillow Property ID (ZPID) and current Zestimate.
        It also includes the date the Zestimate was computed, a valuation range and the Zestimate ranking for the property within its ZIP code.
        The GetSearchResults API Web Service is located at: http://www.zillow.com/webservice/GetSearchResults.htm
        :param zws_id: The Zillow Web Service Identifier. Each subscriber to Zillow Web Services is uniquely identified by an ID sequence and every request to Web services requires this ID.
        :param address: The address of the property to search. This string should be URL encoded.
        :param citystatezip: The city+state combination and/or ZIP code for which to search. This string should be URL encoded. Note that giving both city and state is required. Using just one will not work.
        :param retnzestimat: Return Rent Zestimate information if available (boolean true/false, default: false)
        :return:
        """
        url = '%s/GetSearchResults.htm' % (self.base_url)
        parameters = {'zws-id': zws_id}
        if address and citystatezip:
            parameters['address'] = address
            parameters['citystatezip'] = citystatezip
        else:
            raise ZillowError({'message': "Specify address and citystatezip."})
        if retnzestimate:
            parameters['retnzestimate'] = 'true'

        resp = self._RequestUrl(url, 'GET', data=parameters)
        data = resp.content.decode('utf-8')

        xmltodict_data = xmltodict.parse(data)

        place = Place()
        try:
            place.set_data(xmltodict_data.get('SearchResults:searchresults', None)['response']['results']['result'])
        except:
            raise ZillowError({'message': "Zillow did not return a valid response: %s" % data})

        return place

    def GetZEstimate(self, zws_id, zpid, retnzestimate=False):
        """
        The GetZestimate API will only surface properties for which a Zestimate exists.
        If a request is made for a property that has no Zestimate, an error code is returned.
        Zillow doesn't have Zestimates for all the homes in its database.
        For such properties, we do have tax assessment data, but that is not provided through the API.
        For more information, see our Zestimate coverage.
        :zws_id: The Zillow Web Service Identifier.
        :param zpid: The address of the property to search. This string should be URL encoded.
        :param retnzestimate: Return Rent Zestimate information if available (boolean true/false, default: false)
        :return:
        """
        url = '%s/GetZestimate.htm' % (self.base_url)
        parameters = {'zws-id': zws_id,
                      'zpid': zpid}
        if retnzestimate:
            parameters['retnzestimate'] = 'true'

        resp = self._RequestUrl(url, 'GET', data=parameters)
        data = resp.content.decode('utf-8')

        xmltodict_data = xmltodict.parse(data)

        place = Place()
        try:
            place.set_data(xmltodict_data.get('Zestimate:zestimate', None)['response'])
        except:
            raise ZillowError({'message': "Zillow did not return a valid response: %s" % data})

        return place

    def GetDeepSearchResults(self, zws_id, address, citystatezip, retnzestimate=False):
        """
        The GetDeepSearchResults API finds a property for a specified address.
        The result set returned contains the full address(s), zpid and Zestimate data that is provided by the GetSearchResults API.
        Moreover, this API call also gives rich property data like lot size, year built, bath/beds, last sale details etc.
        :zws_id: The Zillow Web Service Identifier.
        :param address: The address of the property to search. This string should be URL encoded.
        :param citystatezip: The city+state combination and/or ZIP code for which to search.
        :param retnzestimate: Return Rent Zestimate information if available (boolean true/false, default: false)
        :return:

        Example:
        """
        url = '%s/GetDeepSearchResults.htm' % (self.base_url)
        parameters = {'zws-id': zws_id,
                      'address': address,
                      'citystatezip': citystatezip
                      }

        if retnzestimate:
            parameters['retnzestimate'] = 'true'

        resp = self._RequestUrl(url, 'GET', data=parameters)
        data = resp.content.decode('utf-8')

        xmltodict_data = xmltodict.parse(data)

        place = Place(has_extended_data=True)
        try:
            place.set_data(xmltodict_data.get('SearchResults:searchresults', None)['response']['results']['result'])
        except:
            raise ZillowError({'message': "Zillow did not return a valid response: %s" % data})

        return place

    def GetDeepComps(self, zws_id, zpid, count=10, rentzestimate=False):
        """
        The GetDeepComps API returns a list of comparable recent sales for a specified property.
        The result set returned contains the address, Zillow property identifier, and Zestimate for the comparable
        properties and the principal property for which the comparables are being retrieved.
        This API call also returns rich property data for the comparables.
        :param zws_id: The Zillow Web Service Identifier.
        :param zpid: The address of the property to search. This string should be URL encoded.
        :param count: The number of comparable recent sales to obtain (integer between 1 and 25)
        :param rentzestimate: Return Rent Zestimate information if available (boolean true/false, default: false)
        :return:
        Example
            >>> data = api.GetDeepComps("<your key here>", 2100641621, 10)
        """
        url = '%s/GetDeepComps.htm' % (self.base_url)
        parameters = {'zws-id': zws_id,
                      'zpid': zpid,
                      'count': count}
        if rentzestimate:
            parameters['rentzestimate'] = 'true'

        resp = self._RequestUrl(url, 'GET', data=parameters)
        data = resp.content.decode('utf-8')

        # transform the data to an dict-like object
        xmltodict_data = xmltodict.parse(data)

        # get the principal property data
        principal_place = Place()
        principal_data = xmltodict_data.get('Comps:comps')['response']['properties']['principal']

        try:
            principal_place.set_data(principal_data)
        except:
            raise ZillowError({'message': 'No principal data found: %s' % data})

        # get the comps property_data
        comps = xmltodict_data.get('Comps:comps')['response']['properties']['comparables']['comp']

        comp_places = []
        for datum in comps:
            place = Place()
            try:
                place.set_data(datum)
                comp_places.append(place)
            except:
                raise ZillowError({'message': 'No valid comp data found %s' % datum})

        output = {
            'principal': principal_place,
            'comps': comp_places
        }

        return output

    def GetComps(self, zws_id, zpid, count=25, rentzestimate=False):
        """
        The GetComps API returns a list of comparable recent sales for a specified property.
        The result set returned contains the address, Zillow property identifier,
        and Zestimate for the comparable properties and the principal property for which the comparables are being retrieved.
        :param zpid: The address of the property to search. This string should be URL encoded.
        :param count: The number of comparable recent sales to obtain (integer between 1 and 25)
        :param retnzestimate: Return Rent Zestimate information if available (boolean true/false, default: false)
        :return:
        """
        url = '%s/GetComps.htm' % (self.base_url)
        parameters = {'zws-id': zws_id,
                      'zpid': zpid,
                      'count': count}
        if rentzestimate:
            parameters['rentzestimate'] = 'true'

        resp = self._RequestUrl(url, 'GET', data=parameters)
        data = resp.content.decode('utf-8')

        # transform the data to an dict-like object
        xmltodict_data = xmltodict.parse(data)

        # get the principal property data
        principal_place = Place()
        principal_data = xmltodict_data.get('Comps:comps')['response']['properties']['principal']

        try:
            principal_place.set_data(principal_data)
        except:
            raise ZillowError({'message': 'No principal data found: %s' % data})

        # get the comps property_data
        comps = xmltodict_data.get('Comps:comps')['response']['properties']['comparables']['comp']

        comp_places = []
        for datum in comps:
            place = Place()
            try:
                place.set_data(datum)
                comp_places.append(place)
            except:
                raise ZillowError({'message': 'No valid comp data found %s' % datum})

        output = {
            'principal': principal_place,
            'comps': comp_places
        }

        return output

    def _RequestUrl(self, url, verb, data=None):
        """
        Request a url.
        :param url: The web location we want to retrieve.
        :param verb: GET only (for now).
        :param data: A dict of (str, unicode) key/value pairs.
        :return:A JSON object.
        """
        if verb == 'GET':
            url = self._BuildUrl(url, extra_params=data)
            try:
                return requests.get(
                    url,
                    auth=self.__auth,
                    timeout=self._timeout
                )
            except requests.RequestException as e:
                raise ZillowError(str(e))
        return 0

    def _BuildUrl(self, url, path_elements=None, extra_params=None):
        """
        Taken from: https://github.com/bear/python-twitter/blob/master/twitter/api.py#L3814-L3836
        :param url:
        :param path_elements:
        :param extra_params:
        :return:
        """
        # Break url into constituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse(url)

        # Add any additional path elements to the path
        if path_elements:
            # Filter out the path elements that have a value of None
            p = [i for i in path_elements if i]
            if not path.endswith('/'):
                path += '/'
            path += '/'.join(p)

        # Add any additional query parameters to the query string
        if extra_params and len(extra_params) > 0:
            extra_query = self._EncodeParameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query

        # Return the rebuilt URL
        return urlunparse((scheme, netloc, path, params, query, fragment))

    def _EncodeParameters(self, parameters):
        """
        Return a string in key=value&key=value form.
        :param parameters: A dict of (key, value) tuples, where value is encoded as specified by self._encoding
        :return:A URL-encoded string in "key=value&key=value" form
        """

        if parameters is None:
            return None
        else:
            return urlencode(dict([(k, self._Encode(v)) for k, v in list(parameters.items()) if v is not None]))

    def _Encode(self, s):
        if self._input_encoding:
            return str(s, self._input_encoding).encode('utf-8')
        else:
            return str(s).encode('utf-8')

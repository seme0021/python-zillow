#!/usr/bin/env python

import zillow
import pprint

if __name__=="__main__":
    key = ""
    with open("./bin/config/zillow_key.conf", 'r') as f:
        key = f.readline().replace("\n", "")

    address = "3400 Pacific Ave., Marina Del Rey, CA"
    postal_code = "90292"

    api = zillow.ValuationApi()
    data = api.GetSearchResults(key, address, postal_code)

    print data
    print "Hello"

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data.get_dict())


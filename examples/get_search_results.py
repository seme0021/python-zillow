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

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data.get_dict())

    detail_data = api.GetZEstimate(key, data.zpid)

    comp_data = api.GetComps(key, data.zpid)

    pp.pprint(comp_data['comps'][1].get_dict())

    deep_results = api.GetDeepSearchResults(key, "1920 1st Street South Apt 407, Minneapolis, MN", "55454")
    pp.pprint(deep_results.get_dict())
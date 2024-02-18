appid = "corielec-collec-SBX-4428ece0e-4d9be7b5"

from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import statistics



def get_market_eval(keywords):
    import requests
    import json

    # set up the request parameters
    params = {
    'api_key': 'C9041191422E456F9E67DCEC2741C0BA',
    'ebay_domain': 'ebay.com',
    'search_term': keywords,
    'type': 'search',
    'listing_type': 'buy_it_now'
    }

    # make the http GET request to Countdown API
    api_result = requests.get('https://api.countdownapi.com/request', params)

    # print the JSON response from Countdown API
    api_results = api_result.json()
    search_results = api_results.get("search_results")


    all = []

    for item in search_results:
        print(item.get("price").get("value"))
        if "shipping_cost" in item:
            all.append(item.get("price").get("value") - item.get("shipping_cost"))
        else:
            all.append(item.get("price").get("value"))

    return round(statistics.mean(all), 2)



    
        

'''
    try:

        api = Finding(domain="svcs.sandbox.ebay.com", appid=appid, config_file=None)
        response = api.execute('FindPopularItems',
                               {'keywords': "tesla"},
                               "",
                               verb_attrs='itemFilter(1).name=ListingType&  itemFilter(1).value=BIN')
        

        api = Finding(domain="svcs.sandbox.ebay.com", appid=appid, config_file=None)
        response = api.execute('findItemsByKeywords',
                               {'keywords': tuple(keywords)},
                               "",
                               verb_attrs='itemFilter(1).name=ListingType&  itemFilter(1).value=BIN')

        values = []

        if int(response.reply.paginationOutput.totalEntries) > 0:
            for i in response.reply.searchResult.item:
                if i.listingInfo.listingType != "false":
                    if float(i.sellingStatus.currentPrice.value) not in values:
                        values.append(float(i.sellingStatus.currentPrice.value))

                        print(float(i.sellingStatus.currentPrice.value))

        print(statistics.mean(values))

        print(statistics.mean(values))

        return statistics.mean(values)


    except ConnectionError as e:
        print(e)
        print(e.response.dict())
'''
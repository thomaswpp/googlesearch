from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pprint
import json


"""
    Reference:
        https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
        https://github.com/googleapis/google-api-python-client/blob/master/samples/customsearch/main.py
        https://stackoverflow.com/questions/22866579/download-images-with-google-custom-search-api
        https://google-api-client-libraries.appspot.com/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html
        https://stackoverflow.com/questions/11554916/google-custom-search-next-page
        https://developers.google.com/apis-explorer/#p/customsearch/v1/search.cse.list
        https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
"""

class SearchGoogle():

    def __init__(self, api_key, cse_id):
        self.__api_key      = api_key
        self.__cse_id       = cse_id
        self.total_result = 0
        self.total_items  = 0

    def __google_search(self, search_term, **kwargs):

        service = build("customsearch", "v1", 
            developerKey=self.__api_key)

        try:

            res = service.cse().list(
                q=search_term, 
                cx=self.__cse_id, 
                **kwargs
                ).execute()

        except HttpError as e:
            print(e)
            return ""

        else:        
            return res

    def _search_google_images(self, search_term, number_page=1, num=10):
        
        search_args = {
            'num': num, #Valid values are integers between 1 and 10, inclusive.
            'searchType': 'image',
            'fileType': ['png', 'jpg', 'jpeg', 'pdf', 'tiff', 'gif'],
            'safe': 'off',
            'imgSize': 'imgSizeUndefined'
            # "['imgSizeUndefined', 'HUGE', 'ICON', 'LARGE', 'MEDIUM', 'SMALL', 'XLARGE', 'XXLARGE']"

        }

        results = []

        for n in range(number_page):
            res = self.__google_search(
                                    search_term, **search_args)

            if not res or not res.get('items'):
                break

            self.total_result = res['searchInformation']['totalResults']
            
            self.total_items += len(res['items'])

            results.append(res['items'])

            #next page
            search_args.update({'start':res['queries']['nextPage'][0]['startIndex']})


        return results


if __name__ == "__main__":

    from consumer_json import ConsumerJson

    credential = ConsumerJson("credential", "google-search.json")
    cr = credential.consumer_json()
    
    searchGoogle = SearchGoogle(cr['apiKey'], cr['searchEngineID'])

    # results = searchGoogle.search_google_image("janitor")
    results = searchGoogle._search_google_images('"janitor" "cleaning"', 2)

    for res in results:
        for items in res:
            pprint.pprint(items['fileFormat'].split('/')[-1])
            pprint.pprint(items['link'])

from multiprocessing.pool import ThreadPool as Pool
from modules.consumer_json import ConsumerJson
from modules.search_google import SearchGoogle
from modules.download import Download
import argparse
import logging
import pprint
import time

"""
    Reference:
        https://www.ellicium.com/python-multiprocessing-pool-process/
        https://stackoverflow.com/questions/15143837/how-to-multi-thread-an-operation-within-a-loop-in-python
        https://docs.python.org/2/library/multiprocessing.html#using-a-pool-of-workers
"""

#RETORNAR O NUMERO DE IMAGENS ENCONTRADAS
#RETORNAR O NUMERO DE IMAGENS BAIXADAS
#VERIFICAR O USER-AGENTE SE ESTA CORRETO PARA ESTE TIPO DE APLICAÇÃO

class Main():

    def __init__(self, search_term, path='images', number_page=10, pool_size=4):
        self.path = path
        self.search_term = search_term
        self.number_page = number_page
        self.pool_size = pool_size

    def download_image(self, downImage, file_name, url):
        downImage._download_image(self.path, file_name, url)


    def get_name_and_url(self, items, i):

        file_format = items['fileFormat'].split('/')[-1]

        if not file_format:                    
            file_format = 'jpeg'

        if i < 10:
            file_name = '0{0}.{1}'.format(i, file_format)
        else:
            file_name = '{0}.{1}'.format(i, file_format)

        url = items['link']

        return file_name, url

    def print_info(self, logging, url, i):

        midx = 'Id: {0}'.format(i) 
        murl = 'Url: {0}'.format(url)

        pprint.pprint(midx)
        pprint.pprint(murl)

        logging.info(midx)
        logging.info(murl)


    def process(self, logging):

        credential = ConsumerJson("credential", "google-search.json")
        cr         = credential.consumer_json()
        
        searchGoogle = SearchGoogle(cr['apiKey'], cr['searchEngineID'])

        downImage = Download(logging)

        results = searchGoogle._search_google_images(self.search_term, self.number_page)

        pool = Pool(self.pool_size)

        start_time = time.time()
        i = 0
        for res in results:
            for items in res:

                file_name, url = self.get_name_and_url(items, i)

                pool.apply_async(self.download_image, (downImage, file_name, url))

                self.print_info(logging, url, i)

                i += 1

        pool.close()
        pool.join()

        print("--- %s seconds ---" % (time.time() - start_time))

        logging.info('Finished')

    def run(self):

        file_name = self.search_term + '.log'
        logging.basicConfig(filename=file_name, filemode='w', level=logging.DEBUG)
        logging.info('Started')

        self.process(logging)


if __name__ == '__main__':

    # Create the parser
    parser = argparse.ArgumentParser(description='Parameter of the search')
    parser.add_argument('--path', '-p',
                   metavar='path',
                   type=str,
                   required=True,
                   help='the path to save images')

    parser.add_argument('--searchterm', '-st',
           metavar='searchterm',
           type=str,
           required=True,
           help='the search term ')

    parser.add_argument('--numberpage', '-np',
           metavar='numberpage',
           type=int,
           required=True,
           help='the number of pages to search')

    parser.add_argument('--numberthread', '-nt',
           metavar='numberthread',
           type=int,
           required=True,
           help='the number of threads')


    # Execute the parse_args() method
    args          = parser.parse_args()

    path          = args.path
    search_term   = args.searchterm
    number_page   = args.numberpage
    number_thread = args.numberthread


    # path        = 'images'
    # search_term = '"janitor" "cleaning"'
    # search_term = 'janitor cleaning floor'
    # number_page = 10
    #Example de usage:
    #python main.py -p images -st "janitor cleaning floor" -np 1 -nt 4

    downImage = Main(search_term, path, number_page, number_thread)
    
    downImage.run()




        




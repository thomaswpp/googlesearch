import requests
import logging
import random
import shutil
import os

"""
    Reference:
        https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
        https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
"""

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
    "Dnt": "1", 
    "Host": "httpbin.org", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": '', 
}

class Download():

    def __init__(self, logging):
        self.__logging = logging

    def __save_image(self, response, file_name):

        with open(file_name, 'wb') as handle:
            shutil.copyfileobj(response.raw, handle)

    def __request_image(self, url):

        user_agent = random.choice(user_agent_list)

        headers.update({"User-Agent": user_agent})

        try:
            
            response = requests.get(url, stream=True, allow_redirects=True, timeout=5)

        except requests.exceptions.Timeout:
            logging.error("Timeout occurred")
        else:
            if not response.ok:
                msg = "Filed to access image url: {0} ".format(url)
                status_code = "Status code: {0}".format(response.status_code)
                logging.error(msg)
                logging.error(status_code)
            else:
                return response

        return

    def _download_image(self, path, file_name, url):

        if not os.path.exists(path):
            os.mkdir(path) 
            print("Directory '% s' created" % directory) 

        file_name = os.path.join(path, file_name)

        response = self.__request_image(url)
        
        if response:
            self.__save_image(response, file_name)

            del response       


if __name__ == '__main__':

    logging.basicConfig(filename='links_not_working.log', filemode='w', level=logging.DEBUG)
    logging.info('Started')

    d = Download(logging)
    d._download_image('images', 'teste.png', 'https://d1r66lkjsqxswx.cloudfront.net/wp-content/uploads/2016/04/janitorCutout.png')
    d._download_image('images', 'teste.jpg', 'http://bitcheswhobrunch.com/wp-content/uploads/2019/07/LRG_DSC01160-2.jpg')
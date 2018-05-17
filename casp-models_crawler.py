import requests
from bs4 import BeautifulSoup
import argparse


# Constants
url = 'http://predictioncenter.org/download_area/CASP13/server_predictions/'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

pattern = '.tar.gz'


def get_data(target_name, request_url=url, request_headers=headers):
    """Gets this server queue data from the url"""
    r = requests.get(url, headers=headers)

    compressed_models = []
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # Get the information for jobs in queue:
        results = soup.find_all('a')
        for result in results:
            if result and pattern in result['href']:
                if target_name in result['href']:
                    target_url = "%s%s" % (url, result['href'])
                    compressed_models.append(target_url)
    return compressed_models


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("target_name", help="CAPRI-CASP Target name")
    args = parser.parse_args()

    # Get available models online:
    compressed_models = get_data(args.target_name)
    if len(compressed_models):
        # Get the models data:
        print 'Compressed models found for %s target:' % args.target_name
        for models_url in compressed_models:
            print '> ', models_url
            print '>> Downloading...'
            r = requests.get(models_url)
            print len(r.content), 'bytes'
            with open('%s.tar.gz' % args.target_name, 'wb') as f:
                f.write(r.content)
            print '>> Done.'
    else:
        print 'Sorry, no models found'

import requests
from bs4 import BeautifulSoup
import argparse
import json


# Constants
url = 'http://robetta.bakerlab.org/queue.jsp?p=%s&OptionalNotes=&UserName=&Host=&Notes=&SortBy=ID&ID=&rpp=%s&StatusStr=All'
url_job_results = 'http://robetta.bakerlab.org/results.jsp?id=%s'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


def get_data(page_number, num_per_page=100, request_url=url, request_headers=headers):
    """Gets this server queue data from the url"""
    r = requests.get(url % (str(page_number), str(num_per_page)), headers=headers)

    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # Get the information for jobs in queue:
        queue_table = soup.find("form",{"name":"myform"})
        rows = queue_table.find_all("tr")
        server_content = []
        for row in rows:
            if row.has_attr('bgcolor') and row['bgcolor'] == "#eeeeee":
                cells = row.findChildren('td')
                content = {}
                job_id = (cells[1].find("a")).contents[0]
                content['job_id'] = job_id
                status = str(cells[2].contents[0])
                if status != 'Complete':
                    status = (status.replace('<font color="green">','')).replace('</font>', '')
                content['status'] = status
                content['method'] = cells[3].contents[0]
                content['username'] = cells[4].contents[0]
                content['target_name'] = cells[5].contents[0]
                content['length'] = int(cells[6].contents[0])
                content['host'] = cells[8].contents[0]
                content['date'] = cells[9].contents[0]
                server_content.append(content)
        return server_content
    else:
        return None


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("num_pages", type=int, help="Number of pages from the server to scrap")
    parser.add_argument('--items_per_page', nargs='?', const=25, type=int, default=25)
    args = parser.parse_args()

    # Scrap the server:
    jobs_data = []
    for i in range(1, args.num_pages + 1):
        job_data = get_data(i, args.items_per_page)
        print 'Page %d...OK' % (i)
        jobs_data += job_data

    # Save data as JSON:
    with open('robetta.json', 'w') as fp:
        json.dump(jobs_data, fp)

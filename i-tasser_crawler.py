import requests
from bs4 import BeautifulSoup
import argparse
import json


# Constants
url = 'https://zhanglab.ccmb.med.umich.edu/I-TASSER/queue.php?pagenum='

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

pattern = 'http://zhanglab.ccmb.med.umich.edu/I-TASSER/output/'


def get_data(page_number, request_url=url, request_headers=headers):
    """Gets this server queue data from the url"""
    r = requests.get("%s%s" % (url, str(page_number)), headers=headers)

    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # Get the information for jobs in queue:
        queue_table = soup.find("table",{"class":"quetable"})
        rows = queue_table.findChildren(['tr'])
        job_data = []
        for row in rows:
            links = row.find_all('a')
            for a in links:
                if a and pattern in a['href']:
                    cells = row.findChildren('td')
                    if not '.pdb' in a['href']:
                        if len(cells) == 9:
                            id = cells[0].string.strip()
                            protein_name = cells[1].string.strip()
                            length = int(cells[2].string.strip())
                            tm_score = cells[4].string.strip()
                            submission_date = cells[6].string.strip()
                            email = cells[7].string.strip()
                            ip = cells[-1].string.strip()
                            job_data.append({'id':id, 'protein_name':protein_name,
                                             'length':length, 'tm_score':tm_score,
                                             'submission_date':submission_date,
                                             'email':email, 'ip':ip,
                                             'models':[]})
                    else:
                        model_url = a['href'].strip()
                        if not model_url in job_data[-1]['models']:
                            job_data[-1]['models'].append(model_url)
        return job_data
    else:
        return None


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("num_pages", type=int, help="Number of pages from the server to scrap")
    args = parser.parse_args()

    # Scrap the server:
    jobs_data = []
    for i in range(1, args.num_pages + 1):
        job_data = get_data(i)
        print 'Page %d...OK' % (i)
        jobs_data += job_data

    # Save data as JSON:
    with open('i-tasser.json', 'w') as fp:
        json.dump(jobs_data, fp)

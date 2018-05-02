import requests
import re
import os

from PIL import Image
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin
from pprint import pprint

url = 'http://exam.lib.ntu.edu.tw/graduate'


fu = UserAgent()
headers = {'User-Agent': fu.random}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')

results = os.path.abspath('./results')
if not os.path.exists(results):
    os.makedirs(results)

pdfs = soup.find_all('img', class_=re.compile('.*field-icon-application-pdf$'))
for i, pdf in enumerate(pdfs):
    href = pdf.parent['href']
    abs_href = urljoin(resp.url, href)
    file_resp = requests.get(abs_href, headers=headers, stream=True)
    
    filename = os.path.basename(abs_href)
    filename = filename.split('&')[0]
    print('({}/{}) catch the filename {}'.format(i+1, len(pdfs), filename))
    filename = os.path.join(results, filename)

    with open(filename, 'wb') as f:
        for chunk in file_resp.iter_content(2048):
            f.write(chunk)
        print('({}/{}) save file {}'.format(i+1, len(pdfs),filename))


# https://github.com/afunTW/Python-Crawling-Tutorial/blob/master/01_files_website/02_file_crawling.ipynb
# pip install lxml
# pip install fake_useragent
# pip install bs4
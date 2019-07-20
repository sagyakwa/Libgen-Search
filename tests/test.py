from bs4 import BeautifulSoup
import urllib.request
import re
import lxml

home_page = urllib.request.urlopen('http://93.174.95.29/_ads/7D475D8B3A0A1A8F1002A68EF2E8FAD7')
soup = BeautifulSoup(home_page)

# for dl_links in soup.find_all('a', attrs={
#                 'href': re.compile("^http://")}):
#     print(dl_links.get('href'))

for dl_links in soup.find_all('a', attrs={
    'href': re.compile("^/main")}):
    print(dl_links.get('href'))

# for links in soup.find_all('a', attrs={'href': re.compile("^http://")}):
#     print(links.get('href'))
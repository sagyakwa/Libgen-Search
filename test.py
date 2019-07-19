from bs4 import BeautifulSoup
import urllib.request
import re

home_page = urllib.request.urlopen('http://gen.lib.rus.ec/search.php?req=978-1285741550&open=0&res=25&view=simple&phrase=1&column=def')
soup = BeautifulSoup(home_page)
ip_format = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

for links in soup.find_all('a', attrs={'href': [re.compile("(^http://93.174.95.29)"), re.compile("^http://libgen.io/get"), re.compile("^http://libgen.me")]}):
    print(links.get('href'))

# for links in soup.find_all('a', attrs={'href': re.compile("^http://")}):
#     print(links.get('href'))
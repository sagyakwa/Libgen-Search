from bs4 import BeautifulSoup
import re
import requests


class GetLink:
    def __init__(self, isbn):
        self.isbn = isbn
        self.list_of_links = []
        self.search_page = requests.get(f'http://gen.lib.rus.ec/search.php?req={self.isbn}&open=0&res=25'
                                                  f'&view=simple&phrase=1&column=def')
        self.soup = BeautifulSoup(self.search_page.content)

    def from_libgenio(self):
        download_links = []
        prefix = 'http://93.174.95.29'

        # Grab libgen.io links
        for links in self.soup.find_all('a', attrs={
            'href': [re.compile("(^http://93.174.95.29)"), re.compile("^http://libgen.io/get"),
                     re.compile("^http://libgen.me")]}):
            self.list_of_links.append(links.get('href'))
        print(self.list_of_links)

        # Grab first link with description, which also contains the download link
        for first_link in self.list_of_links:
            link_content = requests.get((first_link))
            soup = BeautifulSoup(link_content.content)

            # Grab the download links
            for dl_links in soup.find_all('a', href=True, text='GET'):
                appended_link = prefix + dl_links.get('href')
                download_links.append(appended_link)

        return download_links

    def from_booksdl(self):
        download_links = []

        # Grab booksdl.org links
        for links in self.soup.find_all('a', attrs={
            'href': re.compile("(^http://libgen.io/get)")}):
            self.list_of_links.append(links.get('href'))
        print(self.list_of_links)

        for first_link in self.list_of_links:
            link_content = requests.get((first_link))
            soup = BeautifulSoup(link_content.content)

            # Grab the download links
            for dl_links in soup.find_all('a', href=True, text='GET'):
                appended_link = dl_links.get('href')
                download_links.append(appended_link)

        return download_links


test = GetLink('978-1305088061')
print(test.from_libgenio())

#works but prob each class for libgen.io, libgenpw, booksdl.org



from bs4 import BeautifulSoup
import urllib.request
import urllib5
import re
from collections import deque


class Queue:
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''

    def __init__(self, max_size=100):  # Initialize this queue to the empty queue.
        self._queue = deque(maxlen=max_size)

    def enqueue(self, item):  # Queues the passed item
        self._queue.append(item)

    def dequeue(self):  # Dequeues (i.e., removes) the item at the head of this queue *and* returns this item.
        return self._queue.pop()


class Get:
    def __init__(self, isbn):
        self.isbn = isbn
        self.list_of_links = []
        self.search_page = urllib.request.urlopen(f'http://gen.lib.rus.ec/search.php?req={self.isbn}&open=0&res=25'
                                                  f'&view=simple&phrase=1&column=def')
        self.soup = BeautifulSoup(self.search_page)

    # def soup_it_up(self, link, link_filter):
    #     list_of_links = []
    #     url_page = urllib.request.urlopen(link)
    #     soup_it = BeautifulSoup(url_page)
    #
    #     for url_links in soup_it.find_all('a', attrs={ 'href': re.compile(f"^{link_filter}")}):
    #         list_of_links.append(url_links)
    #
    #     return list_of_links

    def link(self):
        download_links = []

        # Grab the "good" links
        for links in self.soup.find_all('a', attrs={
            'href': [re.compile("(^http://93.174.95.29)"), re.compile("^http://libgen.io/get"),
                     re.compile("^http://libgen.me")]}):
            self.list_of_links.append(links.get('href'))
            print(links.get('href'))
        print(self.list_of_links)

        for first_links in self.list_of_links:
            soup = BeautifulSoup(urllib.request.urlopen(str(first_links)))

            for dl_links in soup.find_all('a', attrs={
                'href': re.compile("^http://")}):
                print(f"Checking {first_links}")
                download_links.append(dl_links.get('href'))
                print(dl_links.get('href'))

        return download_links


test = Get('978-1285741550')
print(test.link())



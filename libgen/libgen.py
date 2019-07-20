from bs4 import BeautifulSoup
import re
import requests
import time
from urllib.parse import urljoin

libgenio = 'http://93.174.95.29'
libgenme = 'http://libgen.me'
booksdl = 'http://libgen.io/get'


class Get:

	def __init__(self, isbn):
		self.isbn = isbn
		self.list_of_links = []
		self.search_page = requests.get(f'http://gen.lib.rus.ec/search.php?req={self.isbn}&open=0&res=25&view=simple'
										f'&phrase=1&column=def', stream=True)
		self.soup = BeautifulSoup(self.search_page.content)

	def link_from(self, mirror=libgenio, href_text='GET'):
		start_time = time.time()
		download_links = []

		for links in self.soup.find_all('a', attrs={
			'href': re.compile(f"(^{mirror})")}):
			self.list_of_links.append(links.get('href'))

		for initial_link in self.list_of_links:
			link_content = requests.get(initial_link, stream=True)
			soup = BeautifulSoup(link_content.content, "lxml")

			for dl_link in soup.find_all('a', href=True, text=href_text):
				if str(dl_link.get('href')).startswith('/main/'):
					download_links.append((libgenio + dl_link.get('href')))
				elif dl_link.get('href').startswith('/item/'):
					download_links.append((libgenme + dl_link.get('href')))
				else:
					download_links.append(dl_link.get('href'))

		elapsed_time = time.time() - start_time
		print(f"Search completed in {elapsed_time} seconds. {len(download_links)} link(s) found.")

		return download_links


from bs4 import BeautifulSoup
import re
import requests

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

	def link_from(self, mirror, href_text, append=False):
		download_links = []

		for links in self.soup.find_all('a', attrs={
			'href': re.compile(f"(^{mirror})")}):
			self.list_of_links.append(links.get('href'))
			print(self.list_of_links)

		for initial_link in self.list_of_links:
			link_content = requests.get(initial_link, stream=True)
			soup = BeautifulSoup(link_content.content, "lxml")

			for dl_link in soup.find_all('a', href=True, text=href_text):
				if append:
					if re.match("^/main/", dl_link.get('href')):
						download_links.append((libgenio + dl_link.get('href')))
					elif re.match("^/item/adv/", dl_link.get('href')):
						download_links.append((libgenme + dl_link.get('href')))
				else:
					download_links.append(dl_link.get('href'))

		return download_links


test = Get('978-1305088061')
print(test.link_from(libgenio, 'GET', append=True))
print(test.link_from(libgenme, 'Get from vault'))
print(test.link_from(booksdl, 'GET'))

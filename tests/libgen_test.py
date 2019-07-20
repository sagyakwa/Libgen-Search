from bs4 import BeautifulSoup
import urllib.request
import re
import lxml
from libgen.libgen import Get

libgenio = 'http://93.174.95.29'
libgenme = 'http://libgen.me'
booksdl = 'http://libgen.io/get'

test = Get('978-1305088061')
l1 = (test.link_from(libgenio, 'GET'))
l2 = (test.link_from(libgenme, 'Get from vault'))
l3 = (test.link_from(booksdl, 'GET'))

all_of_it = l1 + l2 + l3

print(all_of_it)

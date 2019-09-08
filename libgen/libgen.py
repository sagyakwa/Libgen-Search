import sys
import threading
from os.path import join, dirname, abspath

from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMenuBar, QListWidget, QMessageBox
from bs4 import BeautifulSoup
import re
import requests
import time
import webbrowser

from qtpy import uic
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QMainWindow
from modern_ui import styles
from modern_ui import windows

_GUI = join(dirname(abspath(__file__)), 'gui.ui')
libgenio = 'http://93.174.95.29'
zlib = 'https://b-ok.cc'
booksdl = 'http://185.39.10.101'
download_links = []
text_to_link = {}


class Signals(QObject):
	label_signal = pyqtSignal(str)
	disable_widgets_signal = pyqtSignal(bool)
	clear_textbox_signal = pyqtSignal()
	display_links_signal = pyqtSignal(int)


class SearchThread(QRunnable):
	def __init__(self, isbn: object):
		super(SearchThread, self).__init__()
		self.signals = Signals()
		self.isbn = isbn
		self.max_retries = 5
		self.retries = 0
		# self.search = Get(isbn)

	def run(self):
		self.signals.disable_widgets_signal.emit(True)
		self.signals.label_signal.emit("Searching...")
		while True:
			if len(download_links) <= 0 and self.retries <= self.max_retries:
				link1_thread = threading.Thread(target=lambda: Get(self.isbn).link_from(libgenio))
				link2_thread = threading.Thread(target=lambda: Get(self.isbn).link_from(zlib))
				link3_thread = threading.Thread(target=lambda: Get(self.isbn).link_from(booksdl))

				link1_thread.start()
				link2_thread.start()
				link3_thread.start()
				link1_thread.join()
				link2_thread.join()
				link3_thread.join()

				self.retries += 1
			else:
				break

		self.signals.disable_widgets_signal.emit(False)
		self.signals.label_signal.emit('Double click for download')
		self.signals.display_links_signal.emit(len(download_links))


class MainWindow(QMainWindow):
	new_list_widget: QListWidget
	search_thread: SearchThread
	isbn: object

	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = uic.loadUi(_GUI, self)
		self.thread_pool = QThreadPool()
		self.initUi()

	def initUi(self):
		self.center()
		self.setWindowTitle('Textbook Request')
		self.setWindowIcon(QIcon('gui-icon.jpg'))
		self.ui.isbn_textbox.textEdited.connect(lambda: self.ui.listWidget.clear())
		self.ui.isbn_textbox.textEdited.connect(lambda: self.ui.progress_label.setText('Ready'))
		self.ui.actionView_Help.triggered.connect(lambda: webbrowser.open_new_tab('https://sagyakwa.pythonanywhere.com/faq'))
		self.ui.progress_label.setAlignment(Qt.AlignCenter)
		self.ui.progress_label.setText('Ready')

	def center(self):
		frame_gm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		center_point = QApplication.desktop().screenGeometry(screen).center()
		frame_gm.moveCenter(center_point)
		self.move(frame_gm.topLeft())

	def update_label(self, text):
		self.ui.progress_label.setText(text)

	def disable_widgets(self, boolean_val):
		objects = [QLabel, QLineEdit, QMenuBar]
		for item in objects:
			for child in self.findChildren(item):
				if boolean_val and child is not self.ui.progress_label:
					child.setEnabled(False)
					self.ui.get_link_btn.setEnabled(False)
				else:
					child.setEnabled(True)
					self.ui.get_link_btn.setEnabled(True)

	def display_links(self):
		if len(download_links) <= 0:
			self.ui.progress_label.setText('No links found :/')
		else:
			# self.ui.listWidget.setAlternatingRowColors(True)
			counter = 1
			for link in download_links:
				text_line = str(f'Link {counter}')
				text_to_link[text_line] = link
				counter += 1
			for key in text_to_link:
				self.ui.listWidget.addItem(key)
			self.ui.listWidget.itemDoubleClicked.connect(lambda: webbrowser.open_new_tab(text_to_link.get(self.ui.listWidget.currentItem().text())))

	@Slot()
	def on_get_link_btn_clicked(self):
		if re.match(r'978(?:-?\d){10}', self.ui.isbn_textbox.text()):
			download_links.clear()
			text_to_link.clear()
			self.ui.listWidget.clear()
			self.isbn = self.ui.isbn_textbox.text()
			self.search_thread = SearchThread(self.isbn)
			self.search_thread.signals.label_signal.connect(self.update_label)
			self.search_thread.signals.disable_widgets_signal.connect(self.disable_widgets)
			self.search_thread.signals.display_links_signal.connect(self.display_links)

			self.thread_pool.start(self.search_thread)
		else:
			QMessageBox.about(self, 'Error', 'Invalid ISBN number')


class Get:
	def __init__(self, isbn):
		self.isbn = isbn
		self.list_of_links = []
		self.mirrors = ['http://libgen.lc', 'http://gen.lib.rus.ec', 'http://185.39.10.101', 'http://93.174.95.27']
		# Check all the mirrors until we find a working mirror
		for link in self.mirrors:
			self.search_page = requests.get(f'{link}/search.php?req={self.isbn}&open=0&res=25&view=simple'
											f'&phrase=1&column=def', stream=True)
			self.soup = BeautifulSoup(self.search_page.content, 'lxml')
			if self.soup.body.find_all(text='502 Bad Gateway') or self.soup.body.find_all(text='504 Gateway Time-out'):
				# move to the next link if we get a bad gateway
				continue
			else:
				# Stop if we find a working link
				break

	def link_from(self, mirror=libgenio, href_text='GET'):
		start_time = time.time()

		for links in self.soup.find_all('a', attrs={
			'href': re.compile(f"(^{mirror})")}):
			self.list_of_links.append(links.get('href'))

		for initial_link in self.list_of_links:
			link_content = requests.get(initial_link, stream=True)
			soup = BeautifulSoup(link_content.content, "lxml")

			if mirror == libgenio or mirror == booksdl:
				for dl_link in soup.find_all('a', href=True, text=href_text):
					if str(dl_link.get('href')).startswith('/main/'):
						download_links.append((libgenio + dl_link.get('href')))
					elif dl_link.get('href').startswith('http://booksdl.org/'):
						download_links.append((dl_link.get('href')))
			else:
				for dl_link in soup.find_all('a', href=re.compile("/book/")):
					download_links.append(zlib + dl_link.get('href'))

		elapsed_time = time.time() - start_time


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	styles.dark_mode(app)
	window = windows.ModernWindow(MainWindow())
	window.show()
	sys.exit(app.exec_())

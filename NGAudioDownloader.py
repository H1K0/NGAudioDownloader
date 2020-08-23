from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QDialog, QFileDialog, QInputDialog
)
from requests import get as load
from bs4 import BeautifulSoup as parse


class GUI(QMainWindow):
	def __init__(self):
		super().__init__()
		loadUi('GUI/MainWindow.ui',self)
		self.dlbtn.clicked.connect(self.download)

	def download(self):
		# Validating input
		songID=self.input.text()
		page=parse(load(f'https://www.newgrounds.com/audio/listen/{songID}').text,'html.parser')
		if page.find(id='pageerror') is not None:
			self.input.clear()
			return
		songTitle=page.find('title').text
		# Getting download link
		link='http://audio.ngfiles.com/'
		page=str(page)
		i=page.find('audio.ngfiles.com')+len('audio.ngfiles.com/')
		while not link.endswith('.mp3'):
			if page[i]!='\\': link+=page[i]
			i+=1
		# Locating file
		dist=QFileDialog.getSaveFileName(self,'Save File',
										 link.split('/')[-1],
										 'MP3 Audio File (*.mp3)')[0]
		if not dist: return
		# Downloading
		with open(dist,'wb') as out:
			out.write(load(link).content)
		self.input.clear()


if __name__ == '__main__':
    from sys import argv
    app=QApplication(argv)
    ngad=GUI()
    ngad.show()
    app.exec_()
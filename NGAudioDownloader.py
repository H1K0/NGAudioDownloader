import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QDialog, QFileDialog, QInputDialog
)
from PyQt5.Qt import QThread, pyqtSignal
from PyQt5 import QtCore
from requests import get as load
from bs4 import BeautifulSoup as parse
from time import sleep


class GUI(QMainWindow):
	def __init__(self):
		super().__init__()
		loadUi('GUI/MainWindow.ui',self)
		self.dlbtn.clicked.connect(self.download)
		self.inprocess=False

	def download(self):
		self.inprocess=True
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
		file=load(link,stream=True)
		global progress
		progress.label.setText(f'Downloading "{songTitle}"...')
		progress.setWindowTitle(f'Downloading "{songTitle}"...')
		progress.bar.setValue(0)
		progress.show()
		self.thread=DownloadThread(file,dist)
		self.thread.got_chunk.connect(lambda done:progress.bar.setValue(done))
		self.thread.finished.connect(self.thread.finish)
		self.thread.start()
		self.input.clear()
		self.inprocess=False


class ProgressDialog(QDialog):
	def __init__(self):
		super().__init__()
		loadUi('GUI/ProgressDialog.ui',self)
		self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowCloseButtonHint)


class DownloadThread(QThread):
	got_chunk=pyqtSignal(object)

	def __init__(self,file,dist):
		super().__init__()
		self.file,self.dist=file,dist

	def run(self):
		global progress
		total=self.file.headers.get('content-length')
		if total is None: total=-1
		else: total=int(total)
		downloaded=0
		with open(self.dist,'wb') as out:
			for data in self.file.iter_content(chunk_size=max(total//100,1024)):
				downloaded+=len(data)
				out.write(data)
				self.got_chunk.emit(100*downloaded//total)

	def finish(self):
		global progress
		progress.hide()
		self.deleteLater()


if __name__ == '__main__':
    from sys import argv
    app=QApplication(argv)
    ngad=GUI()
    progress=ProgressDialog()
    ngad.show()
    sys.exit(app.exec_())
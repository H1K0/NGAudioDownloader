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

	def download(self):
		# Validating input
		songID=self.input.text()
		page=parse(load(f'https://www.newgrounds.com/audio/listen/{songID}').text,'html.parser')
		if page.find(id='pageerror') is not None:
			self.notification=NotificationDialog('Incorrect input or the song doesn\'t exist!')
			self.notification.exec()
			return
		self.songTitle=page.find('title').text
		# Getting download link
		link='http://audio.ngfiles.com/'
		page=str(page)
		i=page.find('audio.ngfiles.com')+len('audio.ngfiles.com/')
		while not link.endswith('.mp3'):
			if page[i]!='\\': link+=page[i]
			i+=1
		# Locating file
		self.dist=QFileDialog.getSaveFileName(self,'Save File',
										 link.split('/')[-1],
										 'MP3 Audio File (*.mp3)')[0]
		if not self.dist: return
		# Downloading
		self.file=load(link,stream=True)
		self.progress=ProgressDialog()
		self.progress.label.setText(f'Downloading "{self.songTitle}"...')
		self.progress.setWindowTitle(f'Downloading "{self.songTitle}"...')
		self.progress.bar.setValue(0)
		self.progress.exec()

	def keyPressEvent(self,event):
		if event.key()==16777216:
			self.close()


class ProgressDialog(QDialog):
	def __init__(self):
		super().__init__()
		loadUi('GUI/ProgressDialog.ui',self)
		self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowCloseButtonHint)
		self.thread=DownloadThread()
		self.thread.got_chunk.connect(lambda done:self.bar.setValue(done))
		self.thread.finished.connect(self.thread.finish)
		self.thread.start()


class DownloadThread(QThread):
	got_chunk=pyqtSignal(object)

	def __init__(self): super().__init__()

	def run(self):
		total=ngad.file.headers.get('content-length')
		if total is None: total=-1
		else: total=int(total)
		downloaded=0
		with open(ngad.dist,'wb') as out:
			for data in ngad.file.iter_content(chunk_size=max(total//100,1024)):
				downloaded+=len(data)
				out.write(data)
				self.got_chunk.emit(100*downloaded//total)

	def finish(self):
		global ngad
		ngad.progress.hide()
		ngad.notification=NotificationDialog(f'"{ngad.songTitle}" has been downloaded successfully!')
		ngad.notification.exec()
		self.deleteLater()


class NotificationDialog(QDialog):
	def __init__(self,msg):
		super().__init__()
		loadUi('GUI/NotificationDialog.ui',self)
		self.label.setText(msg)
		self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowCloseButtonHint)
		self.btn.clicked.connect(self.accept)

	def accept(self):
		ngad.input.clear()
		self.close()


if __name__ == '__main__':
    from sys import argv
    app=QApplication(argv)
    ngad=GUI()
    ngad.show()
    sys.exit(app.exec_())
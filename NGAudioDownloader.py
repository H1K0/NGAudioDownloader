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
from langswitch import switch
import webbrowser as web
from configer import config


class GUI(QMainWindow):
	def __init__(self):
		super().__init__()
		loadUi('GUI/MainWindow.ui',self)
		self.applylang()
		self.btn.clicked.connect(self.download)
		self.actionSettings.triggered.connect(self.show_settings)
		self.actionHelp.triggered.connect(self.show_help)

	def applylang(self):
		self.title.setText(switch['title'][config["lang"]])
		chfont(self.title,switch['title'][f'font_{config["lang"]}'])
		self.input.setPlaceholderText(switch['placeholder'][config["lang"]])
		chfont(self.input,switch['placeholder'][f'font_{config["lang"]}'])
		self.btn.setText(switch['btn'][config["lang"]])
		chfont(self.btn,switch['btn'][f'font_{config["lang"]}'])
		self.menu.setTitle(switch['menu'][config["lang"]])
		chfont(self.menubar,switch['menu'][f'font_{config["lang"]}'])
		self.actionSettings.setText(switch['settings'][config["lang"]])
		self.actionHelp.setText(switch['helpbtn'][config["lang"]])

	def download(self):
		# Validating input
		songID=self.input.text()
		if not songID:
			self.notification=NotificationDialog(switch['empinp'][config["lang"]])
			self.notification.exec()
			return
		elif not songID.isdigit():
			self.notification=NotificationDialog(switch['typerr'][config["lang"]])
			self.notification.exec()
			return
		page=parse(load(f'https://www.newgrounds.com/audio/listen/{songID}').text,'html.parser')
		if page.find(id='pageerror') is not None:
			self.notification=NotificationDialog(switch['404'][config["lang"]])
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
		self.dist=QFileDialog.getSaveFileName(self,switch['savefile'][config["lang"]],
											  link.split('/')[-1],
											  'MP3 Audio File (*.mp3)')[0]
		if not self.dist: return
		# Downloading
		self.file=load(link,stream=True)
		self.progress=ProgressDialog()
		self.progress.label.setText(switch['downloading'][config["lang"]](self.songTitle))
		self.progress.setWindowTitle(switch['downloading'][config["lang"]](self.songTitle))
		self.progress.bar.setValue(0)
		self.progress.exec()

	def show_settings(self):
		self.settings=SettingsDialog()
		self.settings.exec()

	def show_help(self):
		if config["lang"]=='en': web.open('https://github.com/H1K0/NGAudioDownloader/blob/master/README.md#newgrounds-audio-downloader--',new=2)
		else: web.open(f'https://github.com/H1K0/NGAudioDownloader/blob/master/README-{config["lang"].upper()}.md#newgrounds-audio-downloader--',new=2)

	def keyPressEvent(self,event):
		if event.key()==16777216: self.close()
		elif event.key()==16777220: self.download()


class ProgressDialog(QDialog):
	def __init__(self):
		super().__init__()
		loadUi('GUI/ProgressDialog.ui',self)
		chfont(self.label,switch['downloading'][f'font_{config["lang"]}'])
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
		ngad.notification=NotificationDialog(switch['success'][config["lang"]](ngad.songTitle))
		ngad.notification.exec()
		self.deleteLater()


class NotificationDialog(QDialog):
	def __init__(self,msg):
		super().__init__()
		loadUi('GUI/NotificationDialog.ui',self)
		self.label.setText(msg)
		chfont(self.label,switch['ntf'][f'font_{config["lang"]}'])
		self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowCloseButtonHint)
		ngad.input.clear()
		self.btn.clicked.connect(self.accept)

	def accept(self):
		self.close()


class SettingsDialog(QDialog):
	def __init__(self):
		super().__init__()
		loadUi('GUI/SettingsDialog.ui',self)
		self.setWindowTitle(switch['settings'][config["lang"]])
		self.title.setText(switch['settings'][config["lang"]])
		self.label_lang.setText(switch['lang'][config["lang"]])
		chfont(self.label_lang,switch['lang'][f'font_{config["lang"]}'])
		if config["lang"]=='en':
			self.rbtn_en.setChecked(True)
		elif config["lang"]=='ru':
			self.rbtn_ru.setChecked(True)
		elif config["lang"]=='jp':
			self.rbtn_jp.setChecked(True)
		self.newlang=config["lang"]
		self.rbtn_en.toggled.connect(lambda:self.chlang('en'))
		self.rbtn_ru.toggled.connect(lambda:self.chlang('ru'))
		self.rbtn_jp.toggled.connect(lambda:self.chlang('jp'))
		self.accepted.connect(self.updlang)

	def chlang(self,newlang):
		if newlang!=config["lang"]:
			self.newlang=newlang

	def updlang(self):
		config["lang"]=self.newlang
		ngad.applylang()


def chfont(unit,font): unit.setStyleSheet(f'font-family:{font}')


if __name__ == '__main__':
    from sys import argv
    app=QApplication(argv)
    ngad=GUI()
    ngad.show()
    sys.exit(app.exec_())
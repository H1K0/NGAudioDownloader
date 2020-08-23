from os import access,F_OK,mkdir
from requests import get as load
from bs4 import BeautifulSoup as parse
import click
from sys import stdout


@click.command()
@click.argument('songid',nargs=1,metavar='<Newgrounds song ID>')
@click.option('-d','--dist',default='./Downloads',type=click.Path(exists=True),help='Where to save the songs (default: ./Downloads)')
def CLI(songid,dist):
	"""===== Newgrounds Audio Downloader by H1K0 ====="""
	print('Loading HTML...')
	page=parse(load(f'https://www.newgrounds.com/audio/listen/{songid}').text,'html.parser')
	songTitle=page.find('title').text

	print('Searching download link...')
	link='http://audio.ngfiles.com/'
	page=str(page)
	i=page.find('audio.ngfiles.com')+len('audio.ngfiles.com/')
	while not link.endswith('.mp3'):
		if page[i]!='\\': link+=page[i]
		i+=1

	if not access(dist,F_OK): mkdir(dist)
	print(f'Downloading "{songTitle}"...')
	download(link,dist)
	print(f'"{songTitle}" successfully downloaded.')


def download(link,dist):
	BARLEN=50
	with open(f'{dist}/{link.split("/")[-1]}','wb') as out:
		file=load(link,stream=True)
		total=file.headers.get('content-length')
		if total is None: total=-1
		else: total=int(total)
		downloaded=0
		for data in file.iter_content(chunk_size=max(total//BARLEN,1024)):
			downloaded+=len(data)
			out.write(data)
			done=BARLEN*downloaded//total
			stdout.write(f'\r[{"█"*done}{"·"*(BARLEN-done)}]')
			stdout.flush()
	print()


if __name__=='__main__': CLI()
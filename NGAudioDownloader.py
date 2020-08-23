from os import access,F_OK,mkdir
from requests import get as load
from bs4 import BeautifulSoup as parse

print()

songId=input('Enter song id: ')

print('Loading HTML...')
page=parse(load(f'https://www.newgrounds.com/audio/listen/{songId}').text,'html.parser')
songTitle=page.find('title').text

print('Creating download link...')
dllink=f'http://audio.ngfiles.com/{songId[:3]}000/{songId}_'
count=0
for char in songTitle:
	if 97<=ord(char.lower())<=122:
		dllink+=char
		count+=1
	elif char==' ':
		dllink+='-'
		count+=1
	if count==26:
		break
dllink+='.mp3'

if not access('Downloads',F_OK):
	mkdir('Downloads')

print(f'Downloading "{songTitle}"...')
with open(f'Downloads/{dllink.split("/")[-1]}','wb') as out:
	out.write(load(dllink).content)
print(f'{songTitle} successfully downloaded.')
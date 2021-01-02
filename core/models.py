from django.db import models
from bs4 import BeautifulSoup
import requests



def BrowseMangaName():

	url = 'https://mangahub.io'
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')
	results = soup.find_all(class_="media-left")

	browseResult = []

	for result in results:

		dbManga = {}
		dbManga['name'] = result.find('a')['href'].split('/')[-1].replace('-',' ')
		dbManga['link'] = result.find('a')['href'].split('/')[-1]

		# check if None or not
		if result.find(class_="manga-thumb list-item-thumb-small"):

			dbManga['thumbnail_image'] = result.find(class_="manga-thumb list-item-thumb-small")['src']
		else:
			dbManga['thumbnail_image'] = '-'

		browseResult.append(dbManga)

	print(browseResult)
	return browseResult

	
# ENG

def MH_manga_name(title):

	url = 'https://mangahub.io/search?q='
	
	url = url + f'{title}'
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')
	results     = soup.find_all(class_="media-heading")
	thumbnail_image = soup.find_all(class_="media-left")

	manga_name_results = []

	for num, result in enumerate(results):

		manga = {}
		manga['name']   = result.find('a').text
		manga['latest_chapter'] = result.next_sibling.find('a').text.strip('#')
		manga['status'] = 'Completed' if 'Completed' in result.next_sibling.get_text() else 'Ongoing'
		manga['link'] = result.find('a')['href'].rsplit('/', 1)[-1]
		manga['thumbnail_image'] = thumbnail_image[num].find(class_="manga-thumb")['src']

		manga_name_results.append(manga)

	return manga_name_results



def MH_manga_chapter(title):

	manga_chapter_results = []

	url = 'https://mangahub.io/manga/' 

	url = url + f'{title}'
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')

	# -----------  Summary --------------------------------

	if soup.find(class_="ZyMp7"):
		
		summary = soup.find(class_="ZyMp7").getText()
	else:

		summary = '-'

	if soup.find(class_="img-responsive manga-thumb"):

		cover_img = soup.find(class_="img-responsive manga-thumb")
		cover_img = cover_img['src']

	else:
		cover_img = '-'


	# --------------- list chapter --------------------------


	if soup.find_all(class_="_287KE list-group-item"):
		
		results = soup.find_all(class_="_287KE list-group-item")

		for data in results:

			manga_chapter = {}
			manga_chapter['chapter_name'] = data.find('a')['href'].rsplit('/', 2)[-1]
			manga_chapter['link'] = data.find('a')['href'].rsplit('/', 2)[-1]
			manga_chapter_results.append(manga_chapter)

		# print(manga_chapter_results)

		return manga_chapter_results, summary, cover_img

	manga_chapter_results = '-'

	return manga_chapter_results, summary, cover_img



def MH_manga_image(manga_name, chapter):

	url = f'https://mangahub.io/chapter/'

	url = url + f'{manga_name}' + '/' + f'{chapter}'
	# print(url)
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')
	results = soup.find_all(class_="PB0mN")[0]['src'].rsplit('/1.',1)

	base_url, type_image = results[0] + '/' , '.' + results[-1]
	list_image = []

	for i in range(1, 100):

		manga_url = {}
		manga_url['image'] = base_url + str(i) + type_image
		list_image.append(manga_url)

	return list_image




# IND



def ID_manga_name(title):

	url = 'https://www.maid.my.id/?s='
	
	url = url + f'{title}'
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')

	manga_name_results = []
	results = soup.find_all(class_ = 'flexbox2-content')
	
	for result in results:
	
		manga = {}

		manga['link'] = result.find('a')['href'].split('/')[-2]
		
		for i in result.find_all(class_ = 'flexbox2-thumb'):
		
			manga['name'] = i.find('img')['title']
			manga['thumbnail_image'] = i.find('img')['src']
			manga['status'] = ''

		for i in result.find_all(class_ = 'season'):

			manga['latest_chapter'] = i.text
		
		
		manga_name_results.append(manga)

	# print(manga_name_results)
	return manga_name_results


def ID_manga_chapter(title):

	url = f'https://www.maid.my.id/manga/{title}/'
	# url = url + f'{title}'
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')

	manga_chapter_results = []


	# ----------------------- summary ------------------------------

	if soup.find(class_='series-thumb').find('img')['src']:
		cover_img = soup.find(class_='series-thumb').find('img')['src']

	else:
		cover_img = '-'


	if soup.find(class_='series-synops'):
		summary = soup.find(class_='series-synops').text
	else:
		summary = '-'


	if soup.find(class_='status Ongoing'):
		status = soup.find(class_='status Ongoing').text
	else:

		status = '-'


	# -------------  chapter ----------------------------------------

	if soup.find_all(class_='flexch-infoz'):
		
		results = soup.find_all(class_='flexch-infoz')

		for data in results:

			manga_chapter = {}
			manga_chapter['chapter_name'] = data.find('a')['title']
			manga_chapter['link'] = data.find('a')['href'].split('/')[-2]
			manga_chapter_results.append(manga_chapter)

		print(manga_chapter_results)

		return manga_chapter_results, summary, cover_img, status

	manga_chapter_results = '-'

	return manga_chapter_results, summary, cover_img, status


def ID_manga_image(chapter):

	url = f'https://www.maid.my.id/{chapter}/'
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')

	list_image = []

	results = soup.find_all(class_='reader-area')

	for i in results:
		for data in i.find_all('img'):

			manga_url = {}
			manga_url['image'] = data['src']
			list_image.append(manga_url)

	return list_image
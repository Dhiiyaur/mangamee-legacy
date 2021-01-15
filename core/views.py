from django.shortcuts import render
from django.views.generic import View
from .models import BrowseMangaName
from .models import MH_manga_name, MH_manga_chapter, MH_manga_image
from .models import ID_manga_name, ID_manga_chapter, ID_manga_image
import json
# Create your views here.

class HomeView(View):

    def get(self, request):

        # print(request.COOKIES.get('history'))
        if request.COOKIES.get('history') != None:

            cookies = json.loads(request.COOKIES.get('history'))
            print(cookies)
            template = 'home-history.html'
            return render(request, template, {'cookies' : cookies})
        
        else:

            template = 'home.html'
            return render(request, template)


class BrowserManga(View):

    def get(self, request):

        dbManga = BrowseMangaName()
        print(dbManga)
        template = 'browse.html'
        return render(request, template, {'dbManga' : dbManga})


# -------------   fuction   ------------------------


def SearchBar(request):

# templates 
    templates_search = 'search-page-eng.html'
    templates_search_id = 'search-page-ind.html'
    templates_home   = 'home.html'
    
    # option
    
    lang = request.GET.get('myRadio')
    title = request.GET.get('manga_title')

    if not title:
        return render(request, templates_home)

    if lang == 'ENG':

        manga_data  = MH_manga_name(title)
        context = { 'manga' : manga_data , 'search_title' : title}
        
        return render(request, templates_search, context)

    else:
        
        manga_data = ID_manga_name(title)
        
        context = { 'manga' : manga_data, 'search_title' : title}
        return render(request, templates_search_id, context)




def manga_page(request, manga_name):

    templates = 'manga-page-eng.html'
    templates_eror   = 'error.html'
    
    chapter, summary, cover_img = MH_manga_chapter(manga_name)
    
    if chapter == '-':
        
        return render(request, templates_eror)
                
    context = { 'manga' : chapter, 'manga_name' : manga_name, 'summary' : summary, 'cover_img': cover_img }
    return render(request, templates, context)


def chapter_page(request, manga_name, chapter):

	templates = 'chapter-page-eng.html'
	
	image = MH_manga_image(manga_name, chapter)
	context = {'manga' : image, 'chapter' : chapter }
	return render(request, templates, context)


# IND


def ID_manga_page(request, manga_name):
    
    templates = 'manga-page-ind.html'
    templates_eror   = 'error.html'
    
    chapter, summary, cover_img, status = ID_manga_chapter(manga_name)
    
    if chapter == None:
        
        return render(request, templates_eror)
    
    context = { 'manga' : chapter, 'manga_name' : manga_name, 'summary' : summary, 'cover_img': cover_img, 'status':status }
    return render(request, templates, context)


def ID_chapter_page(request, manga_name, chapter):
    
    templates = 'chapter-page-ind.html'
    templates_eror   = 'error.html'
    
    image = ID_manga_image(chapter)
    context = {'manga' : image }
    return render(request, templates, context)
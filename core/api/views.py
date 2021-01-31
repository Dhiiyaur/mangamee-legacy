from core.models import (
    BrowseMangaName,
    MH_manga_name,
    MH_manga_chapter,
    MH_manga_image,
    ID_manga_name,
    ID_manga_chapter,
    ID_manga_image
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class browseMangaAPI(APIView):

    def get(self, request):

        dbManga = BrowseMangaName()
        respone = Response(dbManga, status=status.HTTP_200_OK)
        return respone


class searchMangaAPI(APIView):

    def get(self, request):

        title = request.GET.get('manga_title')
        lang_select = request.GET.get('lang')

        if lang_select == 'EN':
            result = MH_manga_name(title)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone
        else:
            result = ID_manga_name(title)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone

class chapterMangaAPI(APIView):

    def get(self, request):

        title = request.GET.get('manga_title')
        lang_select = request.GET.get('lang')

        if lang_select == 'EN':

            chapter, summary, cover_img = MH_manga_chapter(title)
            result = {

                'cover_img' : cover_img,
                'summary' : summary,
                'chapters' : chapter
                
            }
            respone = Response(result, status=status.HTTP_200_OK)
            return respone

        else:
            chapter, summary, cover_img, status_manga = ID_manga_chapter(title)
            result = {

                'cover_img' : cover_img,
                'summary' : summary,
                'status': status_manga,
                'chapters' : chapter
                
            }
            respone = Response(result, status=status.HTTP_200_OK)
            return respone


class pageMangaAPI(APIView):

    def get(self, request):

        title = request.GET.get('manga_title')
        chapter = request.GET.get('chapter')
        lang_select = request.GET.get('lang')

        if lang_select == 'EN':
            result = MH_manga_image(title, chapter)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone
        else:
            result = ID_manga_image(chapter)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone

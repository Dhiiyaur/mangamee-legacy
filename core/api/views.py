from core.models import (
    BrowseMangaName,
    MH_manga_name,
    MH_manga_chapter,
    MH_manga_image,
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
        result = MH_manga_name(title)
        respone = Response(result, status=status.HTTP_200_OK)
        return respone

class chapterMangaAPI(APIView):

    def get(self, request):

        title = request.GET.get('manga_title')
        result = MH_manga_chapter(title)
        respone = Response(result, status=status.HTTP_200_OK)
        return respone


class pageMangaAPI(APIView):

    def get(self, request):

        title = request.GET.get('manga_title')
        chapter = request.GET.get('chapter')
        result = MH_manga_image(title, chapter)
        respone = Response(result, status=status.HTTP_200_OK)
        return respone

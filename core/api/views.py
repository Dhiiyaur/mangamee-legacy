from core.models import (
    BrowseMangaName,
    PopularMangaName,
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

import json
import pyrebase
from core.config import *
from rest_framework.parsers import JSONParser 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# user auth  -----------------------------------------------


firebaseConfig = {

    "apiKey"        : apiKey_firebase,
    "authDomain"    : authDomain_firebase,
    "databaseURL"   : databaseUR_firebase ,
    "storageBucket" : storageBucket_firebase

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth    = firebase.auth()
db      = firebase.database()

# --------------------------------------------------------------


class userLoginAPI(APIView):

    def post(self, request):

        data = request.data
        
        # --------------- data params 

        userEmail = data['email']
        userPassword = data['password']

        #----------------------------------

        try:
            user = auth.sign_in_with_email_and_password(userEmail, userPassword)
        except:
            message = {
                'message' : 'account doesnt exist'
            }
            respone = Response(message, status=status.HTTP_404_NOT_FOUND)
            return respone

        token = user['localId']
        userData = {
            'token' : token,

        }
        respone = Response(userData, status=status.HTTP_200_OK)
        return respone


class userRegisterAPI(APIView):

    def post(self, request):

        data = request.data

        # --------------- data params 
        userName = data['username']
        userEmail = data['email']
        userPassword = data['password']

        #----------------------------------
        try:
            user = auth.create_user_with_email_and_password(userEmail, userPassword)

        except:
            message = {
                'message' : 'email already exist'
            }
            respone = Response(message, status=status.HTTP_404_NOT_FOUND)
            return respone
        
        uid  = user['localId']
        data = {

            'name' : userName
        }

        db.child('users').child(uid).set(data)

        message = {
            'message' : 'OK'
        }
        respone = Response(message, status=status.HTTP_200_OK)
        return respone


class userDeleteHistoryAPI(APIView):

    def post(self, request):

        data = request.data
        userToken = data['token']

        userName = db.child("users").get().val().get(userToken).get('name')
        db.child("userHistory").child(userName).remove()

        respone = Response(status=status.HTTP_200_OK)
        return respone


class userUpdateHistoryAPI(APIView):

    def post(self, request):

        data = request.data
        print(data)

        # --------------- data params 

        userToken = data['token']
        userHistory = data['history']

        #----------------------------------
        # print(userToken)
        # print(userHistory)

        userName = db.child("users").get().val().get(userToken).get('name')
        db.child("userHistory").child(userName).set(userHistory)

        respone = Response(status=status.HTTP_200_OK)
        return respone


class userGetHistoryAPI(APIView):

    def post(self, request):

        data = request.data
        # --------------- data params 

        userToken = data['token']
        print(userToken)

        #----------------------------------

        userName = db.child("users").get().val().get(userToken).get('name')

        try:
            userHistory = db.child("userHistory").get().val().get(userName)
            userData = {
                'history' : userHistory,
            }
            
            respone = Response(userData, status=status.HTTP_200_OK)
            return respone

        except:

            respone = Response(status=status.HTTP_404_NOT_FOUND)
            return respone




class browseMangaAPI(APIView):

    def get(self, request):

        dbManga = BrowseMangaName()
        respone = Response(dbManga, status=status.HTTP_200_OK)
        return respone


class popularMangaAPI(APIView):

    def get(self, request):

        try:
            page = request.GET.get('page')
            dbManga = PopularMangaName(page)
            print(dbManga)

            respone = Response(dbManga, status=status.HTTP_200_OK)
            return respone

        except:

            respone = Response(status=status.HTTP_400_BAD_REQUEST)
            return respone

class searchMangaAPI(APIView):


    @method_decorator(cache_page(60*10))
    def get(self, request):

        # --------------- data params 

        title = request.GET.get('manga_title')
        lang_select = request.GET.get('lang')

        # ------------------------------

        if lang_select == 'EN':
            result = MH_manga_name(title)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone
        else:
            result = ID_manga_name(title)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone


class chapterMangaAPI(APIView):

    @method_decorator(cache_page(60*10))
    def get(self, request):

        # --------------- data params 

        title = request.GET.get('manga_title')
        lang_select = request.GET.get('lang')

        # ------------------------------

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

    @method_decorator(cache_page(60*10))
    def get(self, request):

        # --------------- data params 

        title = request.GET.get('manga_title')
        chapter = request.GET.get('chapter')
        lang_select = request.GET.get('lang')

        # ------------------------------

        if lang_select == 'EN':
            result = MH_manga_image(title, chapter)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone
        else:
            result = ID_manga_image(chapter)
            respone = Response(result, status=status.HTTP_200_OK)
            return respone

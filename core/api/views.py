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

import json
import pyrebase
from core.config import *
from rest_framework.parsers import JSONParser 

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




class userGetHistory(APIView):

    def post(self, request):

        data = request.data

        # --------------- data params 

        userToken = data['token']

        #----------------------------------

        userName = db.child("users").get().val().get(userToken).get('name')
        userHistory = db.child("userHistory").get().val().get(userName)

        userData = {

            'history' : userHistory
        }

        respone = Response(userData, status=status.HTTP_200_OK)
        return respone




class browseMangaAPI(APIView):

    def get(self, request):

        dbManga = BrowseMangaName()
        respone = Response(dbManga, status=status.HTTP_200_OK)
        return respone


class searchMangaAPI(APIView):

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

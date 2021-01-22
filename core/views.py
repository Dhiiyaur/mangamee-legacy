from django.shortcuts import render, redirect
from django.views.generic import View
from .models import BrowseMangaName
from .models import MH_manga_name, MH_manga_chapter, MH_manga_image
from .models import ID_manga_name, ID_manga_chapter, ID_manga_image
from .forms import loginUserForm, signupUserForm

import json
import pyrebase
from .config import *
# Create your views here.

# firebase config

firebaseConfig = {

    "apiKey"        : apiKey_firebase,
    "authDomain"    : authDomain_firebase,
    "databaseURL"   : databaseUR_firebase ,
    "storageBucket" : storageBucket_firebase

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth    = firebase.auth()
db      = firebase.database()

# ---------------------------------------------------------------------------------

# Acoount 

class signupUser(View):

    def get(self, request):

        form = signupUserForm()
        template = template = 'account/signup.html'
        return render(request, template, {'form' : form })

    def post(self, request):

        form = signupUserForm(request.POST or None)

        template_login  = 'account/login.html'
        template_signup = 'account/signup.html'

        if form.is_valid():

            email     = form.cleaned_data.get('email')
            userName  = form.cleaned_data.get('userName')
            password1 = form.cleaned_data.get('password1')

            try:
                user = auth.create_user_with_email_and_password(email, password1)

            except:
                message = 'email already exist'
                return render(request, template_signup, {'form' : form, 'message':message })

            uid  = user['localId']
            data = {

                'name' : userName
            }

            db.child('users').child(uid).set(data)
            return redirect('loginUser')
            
        return render(request, template_signup, {'form' : form })


class loginUser(View):

    def get(self, request):

        form = loginUserForm()
        template = 'account/login.html'
        return render(request, template, {'form' : form })

    def post(self,request):

        form = loginUserForm(request.POST or None)
        template = 'account/login.html'

        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = auth.sign_in_with_email_and_password(email, password)
            except:
                message = 'account doesnt exist'
                return render(request, template, {'form' : form, 'message':message })


            # add sesion ID for login
            session_id = user['localId']
            request.session['uid'] = str(session_id)
            # print(request.session['uid'])
            return redirect('syncData')



def logout(request):

    try:
        del request.session['uid']
        
    except :
        pass

    response = redirect('home_page')
    response.delete_cookie('FireBaseHistory')
    return response


def syncData(request):

    uid = request.session['uid']
    userName = db.child("users").get().val().get(uid).get('name')


    try:
        cookies_firebase = db.child("userHistory").get().val().get(userName)
        cookies_firebase_dumps = json.dumps(cookies_firebase)
        request.session['temp'] = cookies_firebase_dumps


    except:
        pass
        
    # return redirect('home_page')
    template = 'account/sync.html'
    return render(request, template, {'userName' : userName})


# -----------------------------------------------------------------------------------------------

class HomeView(View):

    def get(self, request):

        template_history = 'home-history.html'
        template = 'home.html'
 
        try:
            del request.session['temp']
        except:
            pass

        if request.session.has_key('uid'):

            # get user
            
            uid = request.session['uid']
            userName = db.child("users").get().val().get(uid).get('name')

            # get data from local cookies, save to firebase
            if request.COOKIES.get('FireBaseHistory') != None:

                
                cookies = json.loads(request.COOKIES.get('FireBaseHistory'))
                db.child("userHistory").child(userName).set(cookies)

                # fetch history from firebase
    
                return render(request, template_history, {'cookies' : cookies, 'userName' : userName})


            return render(request, template, {'userName' : userName})
        
        
        if request.COOKIES.get('history') != None:

            cookies = json.loads(request.COOKIES.get('history'))
            return render(request, template_history, {'cookies' : cookies})

        return render(request, template)


class BrowserManga(View):

    def get(self, request):

        dbManga = BrowseMangaName()
        template = 'browse.html'

        if request.session.has_key('uid'):

            uid = request.session['uid']
            userName = db.child("users").get().val().get(uid).get('name')
            return render(request, template, {'dbManga' : dbManga, 'userName' : userName})

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
        # return render(request, templates_home)
        return redirect('home_page')

    if lang == 'ENG':

        manga_data  = MH_manga_name(title)
        # print(manga_data)
        if request.session.has_key('uid'):

            uid = request.session['uid']
            userName = db.child("users").get().val().get(uid).get('name')

            context = { 'manga' : manga_data , 'search_title' : title, 'uid' : '1', 'userName' : userName}
            return render(request, templates_search, context)

        context = { 'manga' : manga_data , 'search_title' : title}
        return render(request, templates_search, context)

    else:
        
        manga_data = ID_manga_name(title)

        if request.session.has_key('uid'):

            uid = request.session['uid']
            userName = db.child("users").get().val().get(uid).get('name')

            context = { 'manga' : manga_data, 'search_title' : title, 'uid' : '1', 'userName' : userName}
            return render(request, templates_search_id, context)
        
        context = { 'manga' : manga_data, 'search_title' : title}
        return render(request, templates_search_id, context)




def manga_page(request, manga_name):

    templates = 'manga-page-eng.html'
    templates_eror   = 'error.html'
    
    chapter, summary, cover_img = MH_manga_chapter(manga_name)
    
    if chapter == '-':
        
        return render(request, templates_eror)
    
    if request.session.has_key('uid'):

        uid = request.session['uid']
        userName = db.child("users").get().val().get(uid).get('name')

        context = { 'manga' : chapter, 'manga_name' : manga_name, 'summary' : summary, 'cover_img': cover_img, 'uid' : '1', 'userName' : userName}
        return render(request, templates, context)

    context = { 'manga' : chapter, 'manga_name' : manga_name, 'summary' : summary, 'cover_img': cover_img }
    return render(request, templates, context)


def chapter_page(request, manga_name, chapter):
    templates = 'chapter-page-eng.html'
    last_manga = 'eng' + '-' + manga_name + '/' + chapter
    
    image = MH_manga_image(manga_name, chapter)
    
    if request.session.has_key('uid'):

        uid = request.session['uid']
        userName = db.child("users").get().val().get(uid).get('name')

        context = {'manga' : image, 'chapter' : chapter, 'uid' : '1', 'userName' : userName}
        return render(request, templates, context)
        
    context = {'manga' : image, 'chapter' : chapter}
    return render(request, templates, context)


# IND


def ID_manga_page(request, manga_name):
    
    templates = 'manga-page-ind.html'
    templates_eror   = 'error.html'
    
    chapter, summary, cover_img, status = ID_manga_chapter(manga_name)
    
    if chapter == None:
        
        return render(request, templates_eror)

    
    if request.session.has_key('uid'):

        uid = request.session['uid']
        userName = db.child("users").get().val().get(uid).get('name')

        context = { 'manga' : chapter, 'manga_name' : manga_name, 'summary' : summary, 'cover_img': cover_img, 'status':status, 'uid' : '1', 'userName' : userName}
        return render(request, templates, context)

    context = { 'manga' : chapter, 'manga_name' : manga_name, 'summary' : summary, 'cover_img': cover_img, 'status':status }
    return render(request, templates, context)


def ID_chapter_page(request, manga_name, chapter):
    
    templates = 'chapter-page-ind.html'
    templates_eror   = 'error.html'
    
    image = ID_manga_image(chapter)

    if request.session.has_key('uid'):

        uid = request.session['uid']
        userName = db.child("users").get().val().get(uid).get('name')

        context = {'manga' : image, 'uid' : '1', 'userName' : userName}
        return render(request, templates, context)

    context = {'manga' : image }
    return render(request, templates, context)
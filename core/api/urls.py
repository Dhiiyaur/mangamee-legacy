from django.urls import path
from . import views

# endpoint

urlpatterns = [
    
    path('browse/', views.browseMangaAPI.as_view(), name='browseMangaAPI'),
    path('search/', views.searchMangaAPI.as_view(), name= 'searchMangaAPI'),
    path('manga/', views.chapterMangaAPI.as_view(), name= 'chapterMangaAPI'),
    path('page/', views.pageMangaAPI.as_view(), name= 'PageMangaAPI'),
    path('updatehistory/', views.userUpdateHistoryAPI.as_view(), name= 'userUpdateHistoryAPI'),
    path('gethistory/', views.userGetHistoryAPI.as_view(), name= 'userGetHistoryAPI'),
    path('deletehistory/', views.userDeleteHistoryAPI.as_view(), name= 'userDeleteHistoryAPI'),

    path('auth/login/', views.userLoginAPI.as_view(), name= 'userLoginAPI'),
    path('auth/register/', views.userRegisterAPI.as_view(), name= 'userRegisterAPI'),

]
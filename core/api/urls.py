from django.urls import path
from . import views

# endpoint

urlpatterns = [
    
    path('browse/', views.browseMangaAPI.as_view(), name='browseMangaAPI'),
    path('search/', views.searchMangaAPI.as_view(), name= 'searchMangaAPI'),
    path('manga/', views.chapterMangaAPI.as_view(), name= 'chapterMangaAPI'),
    path('page/', views.pageMangaAPI.as_view(), name= 'PageMangaAPI'),

]
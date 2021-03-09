from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('browse/', views.BrowserManga.as_view(), name = 'browse-manga'),
    path('search/', views.SearchBar, name='search_page'),

    # ENG

    path('manga/<str:manga_name>', views.manga_page, name='manga-page-eng'),
    path('manga/<str:manga_name>/<str:chapter>', views.chapter_page, name='chapter_page'),

   # IND

    path('ID/manga/<str:manga_name>', views.ID_manga_page, name='manga-page-id'),
    path('ID/manga/<str:manga_name>/<str:chapter>', views.ID_chapter_page, name='chapter_page_id'),
    
   # accounts
    
    # path('login/', views.loginUser.as_view(), name='loginUser'),
    # path('signup/', views.signupUser.as_view(), name='signupUser'),
    # path('logout', views.logout, name = 'logoutUser'),
    # path('sync', views.syncData, name = 'syncData'),

 ]
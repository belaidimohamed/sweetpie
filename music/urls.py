from django.urls import path , include
from . import views
app_name="music"
urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('register/',views.Register,name="register"),
    path('login/',views.loginView,name="login"),
    path('logout/',views.logoutView,name="logout"),
    path('addalbum/',views.AlbumCreate.as_view(),name="add-album"),
    path('albums/',views.albums.as_view(),name="albums"),
    path('albums/<int:id>/',views.DetailView.as_view(),name="detail"),
    path('albums/<int:id>/delete',views.DeleteAlbum.as_view(),name="delete-album"),
    path('albums/<int:id>/addsong/',views.CreateSong,name="add-song"),
    path('albums/<int:album_id>/DeleteSong/<int:song_id>',views.DeleteSong,name="song-delete"),
    path('albums/profile/',views.profile.as_view(),name="profile"),
    ]
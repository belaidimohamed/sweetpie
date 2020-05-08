from django.urls import path , include
from . import views
app_name="music"
urlpatterns = [
    path('', views.Index, name="index"),
    path('register/',views.Register,name="register"),
    path('login/',views.loginView,name="login"),
    path('logout/',views.logoutView,name="logout"),

    path('addalbum/',views.AlbumCreate.as_view(),name="add-album"),
    path('albums/',views.albums.as_view(),name="albums"),
    path('albums/<int:id>/',views.DetailView.as_view(),name="detail"),
    path('albums/<int:id>/delete',views.DeleteAlbum.as_view(),name="delete-album"),
    path('albums/<int:id>/addsong/',views.CreateSong,name="add-song"),
    path('albums/<int:album_id>/DeleteSong/<int:song_id>',views.DeleteSong,name="song-delete"),
    
    path('albums/<int:album_id>/song_public/<int:song_id>/',views.song_is_public,name="song_public"),
    path('albums/<int:album_id>/song_favorite/<int:song_id>/',views.song_is_favorite,name="song_favorite"),

    path('albums/<int:album_id>/album_public/',views.album_is_public,name="album_public"),
    path('albums/profile/',views.profile.as_view(),name="profile"),
    path('albums/songs/',views.songs,name="songs"),
    ]
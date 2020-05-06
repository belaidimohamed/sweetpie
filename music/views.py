from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import CreateView , UpdateView , DeleteView , View , DetailView , ListView
from django.urls import reverse_lazy
from .models import Album , Song

from .forms import RegisterForm , LoginForm , SongForm
# Create your views here.

class Index(ListView):
    model = Album
    template_name = "music/index.html"
    context_object_name = "all_albums"
    def get_queryset(self):
        return  Album.objects.all()

class DetailView(DetailView):
    model = Album
    template_name = 'music/detail.html'
    pk_url_kwarg = 'id'

# ---------------------------------------- album shit -------------------------------------------------------

class albums(ListView):
    model = Album
    template_name = "music/albums.html"
    context_object_name = "all_albums"
    def get_queryset(self):
        return  Album.objects.all()
class AlbumCreate(CreateView):
    model = Album
    fields = ['title','artist' ,'album_file']

class DeleteAlbum(DeleteView):
    model = Album
    pk_url_kwarg = 'id'

    success_url = reverse_lazy('music:albums')
#-------------------------------------------- Songs shit -----------------------------------------------------

def CreateSong(request , id):
    form = SongForm(request.POST or None , request.FILES)
    album = get_object_or_404(Album,pk=id)
    if form.is_valid():
        album_songs = album.song_set.all()
        for s in album_songs :
            if s.title == form.cleaned_data.get("title"):
                context={'form':form , 'album':album , 'error_message':'You already made that song !'}
                return render(request, 'music/song_form.html', context)
        song = form.save(commit=False)
        song.album = album
        song.song_file = request.FILES['song_file']
        file_type = song.song_file.url.split('.')[-1].lower()
        AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
        if file_type not in AUDIO_FILE_TYPES : 
            context={'form':form , 'album':album , 'error_message':'Audio file must be WAV, MP3, or OGG'}
            return render(request, 'music/song_form.html', context)
        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context={'form':form , 'album':album }
    return render(request, 'music/song_form.html', context)

def DeleteSong(request , album_id ,song_id):
    album = get_object_or_404(Album,pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request , 'music/detail.html',{'album':album})
# --------------------------------------------- account shit ------------------------------------------------

class profile(ListView):
    model = Album
    template_name = "music/profile.html"
    context_object_name = "all_albums"
    def get_queryset(self):
        return  Album.objects.all()

def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('music:index')
            else:
                return render(request, 'music/account/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/account/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/account/login.html')

def Register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
               
    context = {
        "form": form,
    }
    return render(request, 'music/account/register.html', context)

def logoutView(request):
    logout(request)
    return redirect('music:index')

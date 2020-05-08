from django.shortcuts import render , redirect , get_object_or_404 , render_to_response
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import CreateView , UpdateView , DeleteView , View , DetailView , ListView
from django.urls import reverse_lazy
from .models import Album , Song
from django.db.models import Q


from .forms import RegisterForm , LoginForm , SongForm ,AlbumForm
# Create your views here.

def Index(request):
    albums = Album.objects.all()
    songs = Song.objects.all()
    return render(request, 'music/index.html', {'songs':songs,"all_albums":albums} )

class DetailView(DetailView):
    model = Album
    template_name = 'music/detail.html'
    pk_url_kwarg = 'id'

# ------------------------------------------ album shit -------------------------------------------------------

class albums(ListView):
    model = Album
    template_name = "music/albums.html"
    context_object_name = "all_albums"
    def get_queryset(self):
        return  Album.objects.all()
def albumCreate(request):
    if not request.user.is_authenticated:
        return redirect('music:index')

    form = AlbumForm()
    if request.POST:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = AlbumForm()
            return redirect('music:index')

    return render(request, 'music/album_form.html', {'form':form})

class DeleteAlbum(DeleteView):
    model = Album
    pk_url_kwarg = 'id'

    success_url = reverse_lazy('music:albums')

def album_is_public(request , album_id):
    if not request.user.is_authenticated:
        return redirect('music:login')
    album = get_object_or_404(Album,pk=album_id)
    album.is_public = True
    album.save()
    songs = album.song_set.all()
    for song in songs :
        if song.is_public == False :
            song.is_public = True
            song.save()
        else :
            song.is_public = False
            song.save()
    
    return render(request , 'music/profile.html')



#---------------------------------------------- Songs shit -------------------------------------------------------

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

def song_is_public(request , album_id , song_id):
    if not request.user.is_authenticated:
        return redirect('music:login')
    album = get_object_or_404(Album,pk=album_id)
    song = Song.objects.get(pk=song_id)
    album.is_public = True
    if song.is_public == False :
        song.is_public = True
    else :
        song.is_public = False
    album.save()
    song.save()
    return render(request , 'music/detail.html',{'album':album})

def song_is_favorite(request , album_id , song_id):
    if not request.user.is_authenticated:
        return redirect('music:login')
    album = get_object_or_404(Album,pk=album_id)
    song = Song.objects.get(pk=song_id)
    if song.is_favorite == False :
        song.is_favorite = True
    else :
        song.is_favorite = False
    song.save()
    return render(request , 'music/detail.html',{'album':album})

# --------------------------------------------- account shit ---------------------------------------------------------

def songs(request):
    songs = Song.objects.all()
    x='0'
    if request.POST :
        if request.POST.get('favorite') == "True" :
            x='1'
            songs = Song.objects.filter(is_favorite=request.POST.get('favorite'))

    return render(request, 'music/songs.html', {'songs':songs,'x':x})


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
                return redirect('music:profile')
               
    context = {
        "form": form,
    }
    return render(request, 'music/account/register.html', context)

def logoutView(request):
    logout(request)
    return redirect('music:index')

def getQuerySet(query=None):
    query_set = []
    for q in query.split(" "): # Convert it to list
        posts = Song.objects.filter(Q(title__icontains=q)).distinct()
        for post in posts:
            query_set.append(post)

    return list(set(query_set))

def dropdown(request):
    return render_to_response('music/base.html', {
        'songs': Song.objects.all()
        })
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ProfileForm, SongForm, UserForm
from .models import Profile, Song

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.photo = request.FILES['photo']
            file_type = profile.photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_profile.html', context)
            profile.save()
            return render(request, 'music/detail.html', {'profile':profile})
        context = {
            "form": form,
        }
        return render(request, 'music/create_profile.html', context)


def create_song(request, profile_id):
    form = SongForm(request.POST or None, request.FILES or None)
    profile = get_object_or_404(Profile, pk=profile_id)
    if form.is_valid():
        profile_songs = profile.song_set.all()
        for s in profile_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.profile = profile
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'profile': profile,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'profile': profile})
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)




def delete_song(request, profile_id, song_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'profile': profile})


def detail(request, profile_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, pk=profile_id)
        return render(request, 'music/detail.html', {'profile': profile, 'user': user})


def search_bio(request,profile_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, pk=profile_id)
        return render(request, 'music/search_bio.html', {'profile': profile, 'user': user})

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        profile = Profile.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            profile = profile.filter(
                Q(name__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/search_song.html', {
                'profile': profile,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'profile':profile})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'profile': profile})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
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
                profile= Profile.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'profile': profile})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for profile in Profile.objects.filter(user=request.user):
                for song in profile.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Profile.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })

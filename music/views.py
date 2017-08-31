from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import UpdateView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ProfileForm, SongForm, UserForm
from .models import Profile, Song, LikeDetail
from django.contrib.auth.decorators import login_required

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





class ProfileUpdateView(UpdateView):

    model = Profile
    template_name = 'music/create_profile.html'
    form_class = ProfileForm
    success_url = '/'



def create_song(request, profile_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')


    if request.user.pk == int(profile_id):
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
        #Song_instance = Song.objects.create(likes=0)
        #return render(request, 'create_song.html.html')
    else:
        return render(request,'music/error.html')


def delete_song(request, profile_id, song_id):
    if request.user.pk == int(profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        song = Song.objects.get(pk=song_id)
        song.delete()
        return render(request, 'music/detail.html', {'profile': profile})
    else:
        return render(request, 'music/error.html')

def detail(request, profile_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        if request.user.pk == int(profile_id):
            user = request.user
            profile = get_object_or_404(Profile, pk=profile_id)
            return render(request, 'music/detail.html', {'profile': profile, 'user': user})
        else:
            return render(request, 'music/error.html')


def search_bio(request,profile_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, pk=profile_id)
        return render(request, 'music/detail.html', {'profile': profile, 'user': user})


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


def songs_global(request, filter_by):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            profileid = user.id
            for profile in Profile.objects.all():
                for song in profile.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            like_list = []
            text = 'Like'
            for songid in song_ids:
                liked_flag = 0
                for likedetail in LikeDetail.objects.all():
                    if int(likedetail.profile_id) == int(profileid) and int(likedetail.song_id) == int(songid):
                        liked_flag = 1
                        break
                    else:
                        liked_flag = 0
                if liked_flag == 0:
                    text = 'Like'
                else:
                    text = 'Unlike'
                like_list.append(text)
            print(users_songs)
            print(song_ids)
            print(like_list)
            like_dict = {}
            for i in range(len(users_songs)):
                like_dict[users_songs[i]] = like_list[i]
            print(like_dict)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Profile.DoesNotExist:
            users_songs = []
        return render(request, 'music/song_global.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
            'like_dict': like_dict,
        })

def like_song(request, filter_by, song_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for profile in Profile.objects.all():
                #print(profile)
                for song in profile.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            song = Song.objects.get(pk=song_id)
            profileid = user.id
            likeid = 0
            liked_flag = 0
            for likedetail in LikeDetail.objects.all():
                if int(likedetail.profile_id) == int(profileid) and int(likedetail.song_id) == int(song_id):
                    liked_flag = 1
                    likeid = likedetail.id
                    break
                else:
                    liked_flag = 0
            if liked_flag == 0:
                song.likes = song.likes+1
                song.save()
                LikeDetail.objects.create(profile_id=profileid, song_id = song_id)
            else:
                song.likes = song.likes-1
                song.save()
                likeobject = LikeDetail.objects.get(pk=likeid)
                likeobject.delete()
                liked_flag = 0
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Profile.DoesNotExist:
            users_songs = []
        return render(request, 'music/song_global.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })

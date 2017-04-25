from django.shortcuts import render
from .forms import UserForm,SongForm,ProfileForm
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from .models import Songs,Profile
from django.core.urlresolvers import reverse

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
def index(request):
    return render(request, "music/index.html")

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
                songs = Songs.objects.filter(user=request.user)
                profile=Profile.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'songs': songs,'profile':profile})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    profile=ProfileForm(request.POST or None,request.FILES or None)
    if profile.is_valid():
        pro=profile.save(commit=False)
        pro.name=request.name
        pro.dob=request.dob
        pro.genre=request.genre
        pro.photo=request.FILES('photo')
        pro.hometown=request.hometown
        pro.save()
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
                albums = Songs.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})


    context = {
        "form": form,
        "profile":profile,
    }
    return render(request, 'music/register.html', context)
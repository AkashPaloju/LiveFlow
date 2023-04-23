from django.shortcuts import render, redirect
from app.forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from app.functions import handle_uploaded_file
from app.forms import Uploader
from .models import Video, Watch_later, History, Channel, Pay, BoughtVideoB, MovieSeries, Ad
from django.db.models import Case, When
from django.db.models import Q
import random

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            channel = Channel(name=user.username)
            channel.save()
            print(user.username)
            messages.success(request, "Registration successful." )
            return redirect("app:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("app:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("app:homepage")


def upload(request):
    if request.method == "POST":
        video_name = request.POST['video_name']
        description = request.POST['description']
        tags = request.POST['tags']
        img = request.FILES['img']
        file = request.FILES['file']

        video_model = Video(video_name=video_name, description=description, tags=tags, img=img, file=file)
        video_model.save()

        video1_id = video_model.video_id
        channel_find = Channel.objects.filter(name=request.user)

        for i in channel_find:
            i.video += f" {video1_id}"
            i.save()

        return render(request, "homepage.html")
    return render(request, "upload.html")


def homepage(request):
    video = Video.objects.all()
    context = {'video': video}
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']
        watch = Watch_later.objects.filter(user=user)
        global message
        for i in watch:
            if video_id == i.video_id:
                message = "Video is already in watchlater list"
                break
        else:
            watch_later = Watch_later(user=user, video_id=video_id)
            watch_later.save()
            message = "Video Added To Watchlater"
        cond = True
        videom = Video.objects.filter(video_id=video_id).first()
        video1 = {"videom": videom}
        message1 = {"message": message}
        print(message)
        return HttpResponse({"message": message}, status=204)
    return render(request, "homepage.html", context)


def modify(request):
    global message
    message = ""
    context = {"message", message}
    return render(request, "homepage.html", context)


def videopost(request, id):
    video = Video.objects.filter(video_id=id).first()
    videonew = Video.objects.all()
    ads_available = Ad.objects.all()
    x = video.tags.split()
    ad = random.choice(ads_available)
    for y in ads_available:
        if y.tags in video.tags:
            ad = y
            break
    l = []
    for y in videonew:
        if y.video_id != video.video_id:
            for j in x:
                if j.lower() in y.tags.lower():
                    l.append(y)
                    break

    lx = []
    for x in videonew:
        lx.append(x)

    lx = list(set(lx) - set(l))
    contextnew1 = {"video": video, "lx": lx, "l": l, "ad": ad}
    return render(request, "videopost.html", contextnew1)


def moviepost(request, id):
    video = MovieSeries.objects.filter(movie_id=id).first()
    videonew = MovieSeries.objects.all()
    contextnew1 = {"video": video, "videonew": videonew}
    return render(request, "moviepost.html", contextnew1)


def pay(request):
    if request.method == "POST":
        img = request.FILES['img']
        movie = request.POST['movie']
        pay_model = Pay(name=request.user, movie=movie, img=img)
        pay_model.save()
        return render(request, "homepage.html")
    return render(request, "payment.html")


def comedy(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "comedy.html", context)


def cooking(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "cooking.html", context)


def edu(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "edu.html", context)


def game(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "game.html", context)


def life(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "life.html", context)


def music(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "music.html", context)


def tech(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "tech.html", context)


def travel(request):
    video = Video.objects.all()
    context = {'video': video}
    return render(request, "travel.html", context)


def watch_later(request):
    wl = Watch_later.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)


    preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(ids)])
    video = Video.objects.filter(video_id__in=ids).order_by(preserved)
    return render(request, "watch_later.html", {"video": video})


def history(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']
        # Check if the video ID already exists in the user's history
        historydel = History.objects.filter(user=user, video_id=video_id).first()

        # If it exists, delete the previous entry
        if historydel:
            historydel.delete()
            print("deleted")
        history = History(user=user, video_id=video_id)
        history.save()
        print("saved")
        return redirect(f"/{video_id}")
    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.video_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    video = Video.objects.filter(video_id__in=ids).order_by(preserved)
    return render(request, "history.html", {"history": history, "video": video})


def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.video).split(" ")[1:]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    video = Video.objects.filter(video_id__in=video_ids).order_by(preserved)
    return render(request, "mychannel.html", {"channel": chan, "video": video})

def purchased(request):
    wl = BoughtVideoB.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.movie_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    movie = MovieSeries.objects.filter(movie_id__in=ids).order_by(preserved)
    return render(request, "purchasedvideo.html", {"movie": movie})


def search(request):
    query = request.GET.get("query")
    video = Video.objects.all()
    context = {'video': video}
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']
        watch = Watch_later.objects.filter(user=user)
        global message
        for i in watch:
            if video_id == i.video_id:
                message = "Video is already in watchlater list"
                break
        else:
            watch_later = Watch_later(user=user, video_id=video_id)
            watch_later.save()
            message = "Video Added To Watchlater"
        videom = Video.objects.filter(video_id=video_id).first()
        video1 = {"videom": videom}
        message1 = {"message": message}
        print(message)
        return HttpResponse({"message": message}, status=204)
    qs = video.filter( Q(video_name__icontains=query) |
        Q(tags__icontains=query))
    return render(request, "search.html", {"video": qs, "query": query})


def latest(request):
    video = Video.objects.all()
    context = {'video': video}
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']
        watch = Watch_later.objects.filter(user=user)
        global message
        for i in watch:
            if video_id == i.video_id:
                message = "Video is already in watchlater list"
                break
        else:
            watch_later = Watch_later(user=user, video_id=video_id)
            watch_later.save()
            message = "Video Added To Watchlater"
        videom = Video.objects.filter(video_id=video_id).first()
        video1 = {"videom": videom}
        message1 = {"message": message}
        print(message)
        return HttpResponse({"message": message}, status=204)
    return render(request, "latest.html", context)




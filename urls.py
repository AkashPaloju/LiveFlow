from django.urls import path
from . import views

app_name = "app"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path('upload', views.upload, name="upload"),
    path("<int:id>", views.videopost, name="video post"),
    path("pay", views.pay, name="payment"),
    path("comedy", views.comedy, name="comedy"),
    path("cooking", views.cooking, name="cooking"),
    path("edu", views.edu, name="edu"),
    path("game", views.game, name="game"),
    path("life", views.life, name="life"),
    path("music", views.music, name="music"),
    path("tech", views.tech, name="tech"),
    path("travel", views.travel, name="travel"),
    path("watch_later", views.watch_later, name="watch_later"),
    path("history", views.history, name="history"),
    path("c/<str:channel>", views.channel, name="channel"),
    path("purchased", views.purchased, name="purchase"),
    path("search", views.search, name="search"),
    path("latest", views.latest, name="latest"),
    path("movie/<int:id>", views.moviepost, name="movie"),
]
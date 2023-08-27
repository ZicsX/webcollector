from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start_crawl/", views.start_crawl, name="start_crawl"),
    path("check_status/<str:hash_value>/", views.check_status, name="check_status"),
]

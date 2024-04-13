from django.urls import path,re_path
from tuiliu import views
urlpatterns = [

    path('tuiliu/',views.play_video,name='play_video'),
]
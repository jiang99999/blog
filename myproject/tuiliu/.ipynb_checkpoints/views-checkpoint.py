from django.shortcuts import render
from class_tuiliu import Live

# Create your views here.
def play_video(request):
    # 推流
    live = Live()
    live.run()
    return render(request, 'rtmp.html', {'error_message': "ii"})

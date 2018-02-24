from django.shortcuts import render
from .models import *
from datetime import datetime
from User.models import User, Message
from User.views import get_current_message
# Create your views here.


def index(request):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        username = user.username
    except:
        username = ""
    recent_message = get_current_message()
    info = Game.objects.filter(date=datetime.date(datetime.now())).order_by('id')
    return render(request, "NBAStream/index.html",
                  {'username': username, 'info': info,
                   'recent_message': recent_message})


def gameInfo(request, gameid):
    isLogin = False
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        username = user.username
        isLogin = True
    except:
        userid = ""
        username = ""
    recent_message = get_current_message()
    info = GameInfo.objects.filter(game_id=gameid, orderid__gte=1).order_by('orderid')
    title = Game.objects.get(pk=gameid).title
    if not userid:
        info = info[:1]
    return render(request, 'NBAStream/GameInfo.html',
                  {'username': username, 'title': title,
                   'info': info, 'recent_message': recent_message,
                   'isLogin': isLogin})


def Test(request):
    return render(request, "NBAStream/Temp2.html")

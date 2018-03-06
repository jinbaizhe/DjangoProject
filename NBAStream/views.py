from django.shortcuts import render
from .models import *
from datetime import datetime
from User.models import User
from Web.views import get_current_message, get_recent_visit, get_current_notice
# Create your views here.


def index(request):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
    except:
        user = None
    recent_message = get_current_message()
    info = Game.objects.filter(date=datetime.date(datetime.now())).order_by('id')
    return render(request, "NBAStream/index.html",
                  {'myuser': user, 'info': info,
                   'recent_message': recent_message,
                   'recent_visitor': get_recent_visit(request),
                   'recent_notice': get_current_notice(5)})


def gameInfo(request, gameid):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
    except:
        user = None
    recent_message = get_current_message()
    info = GameInfo.objects.filter(game_id=gameid, orderid__gte=1).order_by('orderid')
    title = Game.objects.get(pk=gameid).title
    if not user:
        info = info[:1]
    return render(request, 'NBAStream/GameInfo.html',
                  {'myuser': user, 'title': title,
                   'info': info,
                   'recent_message': recent_message,
                   'recent_visitor': get_recent_visit(request),
                   'recent_notice': get_current_notice(5)})

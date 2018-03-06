from django.shortcuts import render
from Web.models import *
from datetime import datetime,timedelta
from util.Pagination import *
from django.http import *
# Create your views here.


def notice(request, noticeid):
    try:
        noticeid = int(noticeid)
        notice = Notice.objects.get(id=noticeid)
    except Exception as e:
        raise Http404
    else:
        context = {"item": notice,
                   'recent_message': get_current_message(),
                   'recent_visitor': get_recent_visit(request),
                   'recent_notice': get_current_notice(5)}
        return render(request, "Web/notice.html", context)


def board(request, current_page=1):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
    except:
        user = None
    error_message = ""
    success_message = ""
    if request.POST:
        if not user:
            error_message = "请登录后再发表留言"
        else:
            content = request.POST.get("content")
            if content:
                Message.objects.create(user_id=userid, content=content, createTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                success_message = "发表成功"
            else:
                error_message = "内容不能为空"

    all_message = Message.objects.order_by('-createTime')
    show_message, page_list, current_page, previous_page, next_page, last_page = paginate(all_message, current_page, 5)

    recent_message = get_current_message()
    context = {'success_message': success_message, 'error_message': error_message,
               'show_message': show_message, 'page_list': page_list,
               'current_page': current_page, 'myuser': user,
               'next_page': next_page, 'previous_page': previous_page,
               'last_page': last_page,
               'recent_message': recent_message,
               'recent_visitor': get_recent_visit(request),
               'recent_notice': get_current_notice(5)}
    return render(request, 'Web/board.html', context)


def about(request):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
    except:
        user = None
    return render(request, "Web/about.html", {'myuser': user})


def get_current_message(num=5):
    return Message.objects.order_by("-createTime")[:num]


def get_recent_visit(request, num=5):
    try:
        userid = request.session["userid"]
        user = User.objects.get(id=userid)
    except KeyError:
        user = None
    try:
        ip = request.META["REMOTE_ADDR"]
        user_agent = request.META["HTTP_USER_AGENT"]
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_visit = Visitor.objects.order_by("-visitTime").filter(ip=ip, user=user, visitTime__gt=datetime.now()-timedelta(hours=1))[:1]
        if not last_visit:
            Visitor.objects.create(ip=ip, user_agent=user_agent, user=user,
                                  visitTime=currentTime)
    except KeyError:
        pass
    return Visitor.objects.order_by("-visitTime")[:num]


def get_current_notice(num=5):
    return Notice.objects.order_by("-createTime")[:num]

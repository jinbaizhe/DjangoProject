from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .UserForm import *
from datetime import datetime
from math import ceil
# Create your views here.


def index(request):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        username = user.username
    except:
        username = ""
    return render(request, "User/index.html", {'username': username})


def login(request):
    message = ""
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        autologin = request.POST.get('autologin')
        try:
            user_origin = User.objects.get(username=username)
        except:
            error_message = '用户名不存在'
        else:
            if password == user_origin.password:#验证成功
                response = HttpResponseRedirect(reverse("User:index"))
                request.session['userid'] = user_origin.id
                if not autologin:
                    request.session.set_expiry(0)
                return response
            else:
                error_message = '密码错误'
    return render(request, 'User/login.html', {'message': message, 'error_message': error_message})


def logout(request):
    response = HttpResponseRedirect(reverse("User:login"))
    try:
        del request.session['userid']
    except KeyError:
        pass
    return response


def register(request):
    message = ""
    error_message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if not all((username, password1, password2)):
            error_message = "用户名或密码不能为空"
        elif password1 != password2:
            error_message = "两次密码不一致"
        else:
            try:
                User.objects.get(username=username)
                error_message = "用户名已存在"
            except:
                User.objects.create(username=username,password=password1,
                                    type=0, email=email,
                                    registryTime=datetime.now())
                message = "注册成功"
    context = {'message': message, 'error_message': error_message}
    return render(request, 'User/register.html', context)


def board(request, current_page=1):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        username = user.username
    except:
        userid = ""
        username = ""
    page_size = 5
    page_show_num = 2
    error_message = ""
    success_message = ""
    if request.POST:
        if not username:
            error_message = "请登录后再发表留言"
        else:
            content = request.POST.get("content")
            if content:
                Message.objects.create(user_id=userid, content=content, createTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                success_message = "发表成功"
            else:
                error_message = "内容不能为空"

    message_num = Message.objects.count()
    last_page = ceil(message_num / page_size)

    if current_page < 1:
        current_page = 1
    elif current_page > last_page and last_page != 0:
        current_page = last_page
    beginpos = page_size*(current_page-1)
    all_message = Message.objects.order_by('-createTime')[beginpos:beginpos+page_size]
    begin_show_page = 1
    end_show_page = last_page
    if current_page != 1 and current_page - page_show_num > 1:
        begin_show_page = current_page - page_show_num
    if current_page != last_page and current_page + page_show_num < last_page:
        end_show_page = current_page + page_show_num

    page_list = [x for x in range(begin_show_page, end_show_page + 1)]

    recent_message = get_current_message()
    context = {'success_message': success_message, 'error_message': error_message,
               'all_message': all_message, 'page_list': page_list,
               'current_page': current_page, 'username': username,
               'recent_message': recent_message}
    return render(request, 'User/board.html', context)


def about(request):
    try:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        username = user.username
    except:
        username = ""
    return render(request, "User/about.html", {'username': username})


def get_current_message(num=5):
    return Message.objects.order_by("-createTime")[0:num-1]
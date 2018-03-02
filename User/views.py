from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .UserForm import *
from datetime import *
from math import ceil
from util.Pagination import *
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
                response = HttpResponseRedirect("/")
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
                                    registryTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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

    all_message = Message.objects.order_by('-createTime')
    show_message, page_list, current_page, previous_page, next_page, last_page = paginate(all_message, current_page, 5)

    recent_message = get_current_message()
    context = {'success_message': success_message, 'error_message': error_message,
               'show_message': show_message, 'page_list': page_list,
               'current_page': current_page, 'username': username,
               'next_page': next_page, 'previous_page': previous_page,
               'last_page': last_page, 'recent_message': recent_message,
               'recent_visitor': get_recent_visit(request)}
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


def setting(request, flag="", current_page=1):
    info_error_message = ""
    info_message = ""
    password_error_message = ""
    password_message = ""
    try:
        userid = request.session["userid"]
        user = User.objects.get(id=userid)
        username = user.username
    except Exception as e:
        print(str(e))
    if request.method == "POST":
        if flag == "info":
            try:
                email = request.POST.get("email")
                user.email = email
                user.save()
                info_message = "修改成功"
            except Exception as e:
                info_error_message = str(e)
        elif flag == "password":
            try:
                password_old = request.POST.get("password_old")
                password1 = request.POST.get("password1")
                password2 = request.POST.get("password2")
                if password1!=password2 :
                    password_error_message = "两次输入的密码不一致"
                elif password_old != user.password:
                    password_error_message = "旧密码输入不正确"
                else:
                    user.password = password1
                    user.save()
                    password_message = "修改成功"
            except Exception as e:
                password_error_message = str(e)
    my_all_message = Message.objects.filter(user_id=userid).order_by("-createTime")
    show_my_message, page_list, current_page, previous_page, next_page, last_page = paginate(my_all_message, current_page, 3)
    context = {"flag": flag, 'username': username, 'show_my_message': show_my_message,
               'user': user, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page,
               'info_message': info_message, 'info_error_message': info_error_message,
               'password_message': password_message, 'password_error_message': password_error_message}
    return render(request, "User/setting.html", context)


def get_recent_visit(request, num=5):
    user = None
    try:
        userid = request.session["userid"]
        user = User.objects.get(id=userid)
    except KeyError:
        pass
    try:
        ip = request.META["REMOTE_ADDR"]
        user_agent = request.META["HTTP_USER_AGENT"]
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_visit = Vistor.objects.order_by("-visitTime").filter(ip=ip, user=user, visitTime__gt=datetime.now()-timedelta(hours=1))[:1]
        if not last_visit:
            Vistor.objects.create(ip=ip, user_agent=user_agent, user=user,
                                  visitTime=currentTime)
    except KeyError:
        pass
    return Vistor.objects.order_by("-visitTime")[:num]

from django.shortcuts import render
from Web.models import *
from util.Pagination import *
from django.http import *
from datetime import datetime
# Create your views here.


def validate(request):
    try:
        request.session["adminid"]
    except KeyError:
        return False
    else:
        return True


def index(request):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    return render(request, "Admin/index.html")


def login(request):
    if validate(request):
        return render(request, "Admin/index.html")
    error_message = ""
    success_message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        autologin = request.POST.get('autologin')
        try:
            admin_origin = Administrator.objects.get(username=username)
        except:
            error_message = '用户名不存在'
        else:
            if password == admin_origin.password:#验证成功
                request.session['adminid'] = admin_origin.id
                if not autologin:
                    request.session.set_expiry(0)
                return HttpResponseRedirect("/admin/index")
            else:
                error_message = '密码错误'
    context = {"success_message": success_message, "error_message": error_message}
    return render(request, "Admin/login.html", context)


def logout(request):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    success_message = ""
    try:
        del request.session["adminid"]
    except Exception as e:
        pass
    else:
        success_message = "退出成功"
    context = {"success_message": success_message}
    return render(request, "Admin/login.html", context)


def visit(request, current_page=1):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    all_visitor = Visitor.objects.order_by("-visitTime")
    show_visitor, page_list, current_page, previous_page, next_page, last_page = paginate(all_visitor, current_page, 5)
    context = {'show_visitor': show_visitor, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/visit.html", context)


def notice(request, current_page=1):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    try:
        current_page = int(current_page)
    except TypeError:
        current_page = 1
    page_size = 3
    error_message = ""
    success_message = ""
    if request.method == "POST":
        if not validate(request):
            context = {"success_message": "", "error_message": "请先登录"}
            return render(request, "Admin/login.html", context)
        title = request.POST.get("title")
        content = request.POST.get("content")
        adminid = request.session["adminid"]
        admin = Administrator.objects.get(id=adminid)
        try:
            notice = Notice.objects.create(title=title, content=content,
                                           createTime=datetime.now(), admin=admin)
            notice.save()
        except Exception as e:
            error_message = "发表失败："+str(e)
        else:
            success_message = "发表成功"
    all_notice = Notice.objects.all().order_by("-createTime")
    show_notice, page_list, current_page, previous_page, next_page, last_page = paginate(all_notice, current_page, page_size)
    context = {'success_message': success_message, "error_message": error_message,
               'show_notice': show_notice, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/notice.html", context)


def delete_notice(request, noticeid):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    delete_error_message = ""
    delete_success_message = ""
    try:
        notice = Notice.objects.all().get(id=noticeid)
        notice.delete()
        delete_success_message = "删除成功"
    except Exception as e:
        delete_error_message = str(e)
    all_notice = Notice.objects.all().order_by("-createTime")
    show_notice, page_list, current_page, previous_page, next_page, last_page = paginate(all_notice, 1, 5)
    context = {'delete_success_message': delete_success_message, "delete_error_message": delete_error_message,
               'show_notice': show_notice, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/notice.html", context)


def changepassowrd(request):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    error_message = ""
    success_message = ""
    if request.method == "POST":
        try:
            admin = Administrator.objects.get(id=request.session.get("adminid"))
            password_old = request.POST.get("password_old")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 != password2:
                error_message = "两次输入的密码不一致"
            elif password_old != admin.password:
                error_message = "旧密码输入不正确"
            else:
                admin.password = password1
                admin.save()
                success_message = "修改成功"
        except Exception as e:
            error_message = str(e)
    context = {"error_message": error_message, "success_message": success_message}
    return render(request, "Admin/changePassword.html", context)


def message(request, current_page=1):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    try:
        current_page = int(current_page)
    except TypeError:
        current_page = 1
    page_size = 5
    error_message = ""
    success_message = ""
    all_message = Message.objects.all().order_by("-createTime")
    show_message, page_list, current_page, previous_page, next_page, last_page = paginate(all_message, current_page, page_size)
    context = {'success_message': success_message, "error_message": error_message,
               'show_message': show_message, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/message.html", context)


def delete_message(request, messageid):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录"}
        return render(request, "Admin/login.html", context)
    delete_error_message = ""
    delete_success_message = ""
    try:
        message = Message.objects.all().get(id=messageid)
        message.delete()
        delete_success_message = "删除成功"
    except Exception as e:
        delete_error_message = str(e)
    all_message = Message.objects.all().order_by("-createTime")
    show_message, page_list, current_page, previous_page, next_page, last_page = paginate(all_message, 1, 5)
    context = {'delete_success_message': delete_success_message, "delete_error_message": delete_error_message,
               'show_message': show_message, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/message.html", context)

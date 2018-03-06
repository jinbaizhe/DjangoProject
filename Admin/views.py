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
        try:
            userid = request.session["userid"]
        except KeyError:
            return False
        else:
            user = User.objects.get(id=userid)
            if user.type == 0:
                return False
            elif user.type == 1:
                return True
    else:
        return True


def index(request):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
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
        user_type = request.POST.get('type')
        try:
            if user_type == "admin":
                admin_origin = Administrator.objects.get(username=username)
            elif user_type == "user":
                admin_origin = User.objects.get(username=username)
        except:
            error_message = '用户名不存在'
        else:
            if password == admin_origin.password:#验证成功
                if user_type == "admin":
                    request.session['adminid'] = admin_origin.id
                elif user_type == "user":
                    request.session['userid'] = admin_origin.id
                if not autologin:
                    request.session.set_expiry(0)
                return HttpResponseRedirect("/admin/index")
            else:
                error_message = '密码错误'
    context = {"success_message": success_message, "error_message": error_message}
    return render(request, "Admin/login.html", context)


def logout(request):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    success_message = ""
    try:
        del request.session["adminid"]
    except Exception as e:
        del request.session["userid"]
    else:
        success_message = "退出成功"
    context = {"success_message": success_message}
    return render(request, "Admin/login.html", context)


def visit(request, current_page=1, success_message="", error_message=""):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    all_visitor = Visitor.objects.order_by("-visitTime")
    show_visitor, page_list, current_page, previous_page, next_page, last_page = paginate(all_visitor, current_page, 5)
    context = {'success_message': success_message, "error_message": error_message,
               'show_visitor': show_visitor, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/visit.html", context)


def delete_visitor(request, visitorid):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    error_message = ""
    success_message = ""
    try:
        visitor = Visitor.objects.get(id=visitorid)
        visitor.delete()
    except Exception as e:
        error_message = "删除失败：" + str(e)
    else:
        success_message = "删除成功"
    return visit(request, 1, success_message=success_message,error_message=error_message)


def notice(request, current_page=1, success_message="", error_message=""):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    try:
        current_page = int(current_page)
    except TypeError:
        current_page = 1
    page_size = 3
    if request.method == "POST":
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
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    error_message = ""
    success_message = ""
    try:
        notice_temp = Notice.objects.get(id=noticeid)
        notice_temp.delete()
        success_message = "删除成功"
    except Exception as e:
        error_message = "删除失败："+str(e)
    return notice(request, current_page=1, success_message=success_message, error_message=error_message)


def changepassowrd(request):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
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
            error_message = "修改失败："+str(e)
    context = {"error_message": error_message, "success_message": success_message}
    return render(request, "Admin/changePassword.html", context)


def message(request, current_page=1, success_message="", error_message=""):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    try:
        current_page = int(current_page)
    except TypeError:
        current_page = 1
    page_size = 5
    all_message = Message.objects.all().order_by("-createTime")
    show_message, page_list, current_page, previous_page, next_page, last_page = paginate(all_message, current_page, page_size)
    context = {'success_message': success_message, "error_message": error_message,
               'show_message': show_message, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/message.html", context)


def delete_message(request, messageid):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    error_message = ""
    success_message = ""
    try:
        message_temp = Message.objects.get(id=messageid)
        message_temp.delete()
        success_message = "删除成功"
    except Exception as e:
        error_message = "删除失败："+str(e)
    return message(request, 1, success_message, error_message)


def userSetting(request, current_page=1, success_message="", error_message=""):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    try:
        current_page = int(current_page)
    except TypeError:
        current_page = 1
    page_size = 5
    all_user = User.objects.all().order_by("-registryTime")
    show_user, page_list, current_page, previous_page, next_page, last_page = paginate(all_user, current_page, page_size)
    context = {'success_message': success_message, "error_message": error_message,
               'show_user': show_user, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/userSetting.html", context)


def setAdmin(request, userid):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    error_message = ""
    success_message = ""
    try:
        user = User.objects.get(id=userid)
        user.type = 1
        user.save()
    except Exception as e:
        error_message = "操作失败："+str(e)
    else:
        success_message = "操作成功"
    return userSetting(request, 1, success_message=success_message,error_message=error_message)


def resetAdmin(request, userid):
    if not validate(request):
        context = {"success_message": "", "error_message": "请先登录账号或该账号没有权限"}
        return render(request, "Admin/login.html", context)
    error_message = ""
    success_message = ""
    try:
        user = User.objects.get(id=userid)
        user.type = 0
        user.save()
    except Exception as e:
        error_message = "操作失败："+str(e)
    else:
        success_message = "操作成功"
    return userSetting(request, 1, success_message=success_message,error_message=error_message)


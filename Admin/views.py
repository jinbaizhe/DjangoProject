from django.shortcuts import render
from User.models import *
from util.Pagination import *
# Create your views here.


def index(request):
    return render(request, "Admin/index.html")


def login(request):
    return render(request, "Admin/login.html")


def visit(request, current_page=1):
    all_visitor = Vistor.objects.order_by("-visitTime")
    show_visitor, page_list, current_page, previous_page, next_page, last_page = paginate(all_visitor, current_page, 5)
    context = {'show_visitor': show_visitor, 'page_list': page_list,
               'current_page': current_page, 'next_page': next_page,
               'previous_page': previous_page, 'last_page': last_page}
    return render(request, "Admin/visit.html", context)

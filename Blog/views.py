from django.shortcuts import render
from Blog.models import BlogPost
from datetime import datetime
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
def index(request):
    posts = BlogPost.objects.all()
    return HttpResponse("<h1>暂未完成</h1>")
def posting(request):
    if request.method == 'POST':
        post = BlogPost()
        post.title = request.POST.get("title")
        post.body = request.POST.get("content")
        post.timestamp = datetime.now()
        post.save()
        print(datetime.now)
    return HttpResponseRedirect('/blog/index/')
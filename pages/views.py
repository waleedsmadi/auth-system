from django.shortcuts import render
from posts.models import Post

def index(request):
    posts = Post.objects.all()
    return render(request, 'pages/index.html', {'posts': posts})

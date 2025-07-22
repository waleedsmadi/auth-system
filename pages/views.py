from django.shortcuts import render
from posts.models import Post
from core.decorators import required_login

@required_login
def index(request):
    posts = Post.objects.all()
    return render(request, 'pages/index.html', {'posts': posts})

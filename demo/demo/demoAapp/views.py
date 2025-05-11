from django.shortcuts import render, redirect
from demoAapp.forms import PostForm
from demoAapp.models import Post

def index(request):
    posts = Post.objects.order_by("title")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = PostForm()

    return render(request, "index.html", context={
        'posts': posts,
        'form': form
    })

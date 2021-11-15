from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm
from django.shortcuts import render

# Create your views here.


def index(request):
    # if the method is post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # if the form is validif
        if form.is_valid():
            #yes, save
            form.save()

            # redirect to home
            return HttpResponseRedirect('/')
        else:
            # no, show error
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts , limit=20
    posts = Post.objects.all().order_by('-created_at')[:20]
    form = PostForm()

    # show
    return render(request, 'posts.html',
                  {'posts': posts})


def delete(request, post_id):
    # Find post
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def likes(request, id):
    likedtweet = Post.objects.get(id=id)
    likedtweet.like_count += 1
    likedtweet.save()
    return HttpResponseRedirect('/')


def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())
    form = PostForm
    return render(request, 'edit.html', {'post': post, 'form': form})

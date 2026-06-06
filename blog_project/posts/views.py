from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Category, Post


def home(request):
    latest_posts = Post.objects.filter(is_published=True).select_related(
        "author",
        "category"
    )[:4] #取前四篇bolg

    categories = Category.objects.all()

    return render(request, "posts/home.html", {
        "latest_posts": latest_posts,
        "categories": categories,
    })


def post_list(request):
    posts = Post.objects.filter(is_published=True).select_related(
        "author",
        "category"
    )
    #获取帖子
    categories = Category.objects.all()

    #获取分类参数
    category_slug = request.GET.get("category")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    return render(request, "posts/post_list.html", {
        "posts": posts,
        "categories": categories,
        "selected_category": category_slug,
    })


def post_detail(request, pk):
    #查询数据库有无该帖子
    post = get_object_or_404(
        Post.objects.select_related("author", "category"),
        pk=pk,
        is_published=True
    )

    user_liked = False

    #判断用户是否登录以及点赞帖子
    if request.user.is_authenticated:
        user_liked = post.likes.filter(id=request.user.id).exists()

    return render(request, "posts/post_detail.html", {
        "post": post,
        "user_liked": user_liked,
    })


@login_required   #登陆后访问
def add_post(request):
    #传给form
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(request, "posts/post_form.html", {
        "form": form,
    })


@login_required
@require_POST #通过post请求点赞，更安全
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("post_detail", pk=post.pk) #返回详情页
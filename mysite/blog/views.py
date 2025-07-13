from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404


# Create your views here.
def post_list(request):
    posts = Post.drafts.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        published_at__year=year,
        published_at__month=month,
        published_at__day=day,
        status=Post.Status.DRAFT
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )

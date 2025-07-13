from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404, render
from .models import Post


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
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
        status=Post.Status.PUBLISHED
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )

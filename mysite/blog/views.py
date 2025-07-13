from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from .models import Post
from django.views.generic import ListView

# Create your views here
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number_str = request.GET.get('page', '1')

        try:
            page_number = int(page_number_str)
            # Dieser Aufruf validiert die Seitenzahl. Er löst EmptyPage aus,
            # wenn die Zahl außerhalb des gültigen Bereichs liegt.
            paginator.page(page_number)
        except ValueError:
            # Wenn 'page' keine Ganzzahl ist, leite zur ersten Seite weiter.
            return redirect(reverse('blog:post_list'))
        except EmptyPage:
            # Wenn die Seitenzahl eine Ganzzahl, aber außerhalb des Bereichs ist.
            if page_number > paginator.num_pages:
                # Wenn sie zu hoch ist, leite zur letzten Seite weiter.
                return redirect(reverse('blog:post_list') + f'?page={paginator.num_pages}')
            else:
                # Wenn sie zu niedrig ist (z.B. 0), leite zur ersten Seite weiter.
                return redirect(reverse('blog:post_list'))

        # Wenn alle Prüfungen bestanden wurden, ist die Seitenzahl gültig.
        # Wir überlassen der get()-Methode der Elternklasse die weitere Bearbeitung.
        return super().get(request, *args, **kwargs)



# def post_list(request):
#     post_list_queryset = Post.published.all()
#     paginator = Paginator(post_list_queryset, 3)
#     page_number = request.GET.get('page', '1')
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page_number is not an integer, deliver the first page.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page_number is out of range, deliver last page of results.
#         posts = paginator.page(paginator.num_pages)
#
#     return render(
#         request,
#         'blog/post/list.html',
#         {'posts': posts}
#     )

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

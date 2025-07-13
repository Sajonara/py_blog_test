from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # <-- PageNotAnInteger importieren
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from .models import Post

# Create your views here
def post_list(request):
    post_list_queryset = Post.published.all()
    paginator = Paginator(post_list_queryset, 3)
    
    page_number_str = request.GET.get('page', '1') # Hole den Wert als String
    
    try:
        # Versuche, die angefragte Seite zu laden.
        # Hier übergeben wir den String direkt an paginator.page().
        # Wenn es keine Zahl ist, wird PageNotAnInteger geworfen.
        # Wenn es eine Zahl ist, aber außerhalb des Bereichs, wird EmptyPage geworfen.
        posts = paginator.page(page_number_str)
    except PageNotAnInteger:
        # Wenn die Seitenzahl keine Ganzzahl ist (z.B. 'abc'),
        # leite zur ersten Seite um.
        return redirect(reverse('blog:post_list') + '?page=1')
    except EmptyPage:
        # Wenn die Seitenzahl eine Zahl war, aber außerhalb des Bereichs liegt (z.B. 0, -5, oder 999)
        # Hier ist es wichtig, die ursprüngliche angefragte Zahl zu kennen,
        # um zwischen "zu hoch" und "zu niedrig" zu unterscheiden.
        # Da paginator.page() schon PageNotAnInteger für Non-Integer abgefangen hat,
        # muss page_number_str hier eine gültige Zahl sein.
        
        # Sicherstellen, dass wir eine Zahl zum Vergleichen haben
        # Das int() sollte hier klappen, da PageNotAnInteger schon gefangen wurde
        page_number_int = int(page_number_str) 

        if page_number_int > paginator.num_pages:
            # Wenn zu hoch, leite zur letzten Seite um.
            return redirect(reverse('blog:post_list') + '?page=' + str(paginator.num_pages))
        elif page_number_int < 1:
            # Wenn zu niedrig (<=0), leite zur ersten Seite um.
            return redirect(reverse('blog:post_list') + '?page=1')
        else:
            # Dieser else-Zweig sollte nach den obigen Checks und EmptyPage theoretisch nicht erreicht werden.
            raise Http404("Seite nicht gefunden.")
    
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

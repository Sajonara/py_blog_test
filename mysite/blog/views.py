from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from .models import Post
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib import messages
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail



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

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {'post': post, 'comments': comments, 'form': form}
    )

def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"schlägt Dir vor, {post.title} zu lesen"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            # send email
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            messages.success(request, f'"{post.title}" wurde erfolgreich an {cd["to"]} gesendet.')
            return redirect(post.get_absolute_url())
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {'post': post, 'form': form}
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
        messages.success(request, 'Dein Kommentar wurde erfolgreich hinzugefügt.')
        return redirect(post.get_absolute_url())
    return render(
        request,
        'blog/post/comment.html',
        {'post': post, 'form': form, 'comment': None}
    )
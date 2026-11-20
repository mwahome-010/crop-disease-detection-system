from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import ForumPost, Comment, Flair
from .forms import ForumPostForm, CommentForm, ReplyForm
from django.core.exceptions import PermissionDenied


def can_manage_forum_content(user, author):
    """
    Check whether a user owns the content or is an administrator.
    """
    return (
        user == author
        or user.is_staff
        or user.is_superuser
        or user.role == 'ADMINISTRATOR'
    )


def forum(request):
    """
    Public forum page.
    Guests and logged-in users can view all posts.
    """
    posts = ForumPost.objects.select_related(
        'author', 'flair'
    ).all()

    return render(
        request,
        'forum/forum.html',
        {'posts': posts}
    )


def post_detail(request, post_id):
    """
    Public page showing one post, its comments and replies.
    """
    post = get_object_or_404(
        ForumPost.objects.select_related('author', 'flair'),
        id=post_id
    )

    comments = post.comments.select_related(
        'author'
    ).prefetch_related(
        'replies__author'
    )

    return render(
        request,
        'forum/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_form': CommentForm(),
            'reply_form': ReplyForm(),
        }
    )


@login_required
def create_post(request):
    """
    Only logged-in users can create forum posts.
    """
    if request.method == 'POST':
        form = ForumPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            new_flair_name = form.cleaned_data.get('new_flair')

            if new_flair_name:
                existing_flair = Flair.objects.filter(
                    name__iexact=new_flair_name
                ).first()

                if existing_flair:
                    post.flair = existing_flair
                else:
                    post.flair = Flair.objects.create(
                        name=new_flair_name
                    )

            post.save()

            return redirect('post_detail', post_id=post.id)

    else:
        form = ForumPostForm()

    return render(
        request,
        'forum/create_post.html',
        {'form': form}
    )


@login_required
@require_POST
def add_comment(request, post_id):
    """
    Only logged-in users can comment on posts.
    """
    post = get_object_or_404(ForumPost, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect('post_detail', post_id=post.id)


@login_required
@require_POST
def add_reply(request, comment_id):
    """
    Only logged-in users can reply to comments.
    Replies cannot receive replies.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    form = ReplyForm(request.POST)

    if form.is_valid():
        reply = form.save(commit=False)
        reply.comment = comment
        reply.author = request.user
        reply.save()

    return redirect(
        'post_detail',
        post_id=comment.post.id
    )
import logging
from smtplib import SMTPException
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from .filters import PostFilter
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import PostForm, CommentForm
from django.core.mail import send_mail
logger = logging.getLogger('django')
from .models import Subscription, Category, Post, Comment
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
import django_filters
class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = ['post']

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.get_or_create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')

    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions})





class UserCommentListView(PermissionRequiredMixin, ListView):
    permission_required = ('board.view_comment',)
    model = Comment
    template_name = 'board/user_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(post__user=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CommentAcceptView(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_comment',)
    model = Comment
    fields = []
    template_name = 'board/comment_accept.html'

    def form_valid(self, form):
        comment = self.get_object()
        if not comment.accepted:  # Проверка состояния отклика
            comment.accepted = True
            comment.save()
            try:
                send_mail(
                    subject='Ваш отклик был принят',
                    message=f'Ваш отклик на объявление "{comment.post.title}" был принят.',
                    from_email='vitalivoloshin1975@yandex.co.il',
                    recipient_list=[comment.user.email],
                )
                logger.info("Email sent successfully")
            except SMTPException as e:
                logger.error(f"SMTPException: {e}")
            except Exception as e:
                logger.error(f"Exception: {e}")
        else:
            logger.info("Comment already accepted")
        return super().form_valid(form)

    def get_success_url(self):
        logger.info("Redirecting to comment list")
        return reverse_lazy('board:comment-list')



class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_comment',)
    model = Comment
    template_name = 'board/comment_delete.html'
    success_url = reverse_lazy('board:user_comments')


class CommentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_comment',)
    form_class = CommentForm
    model = Comment
    template_name = 'board/post_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post_id'] = self.kwargs.get('pk')
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs.get('pk')
        response = form.save()
        send_mail(
            subject='Новый отклик',
            message=f'Вы получили новый отклик: {response.content}',
            from_email='vitalivoloshin1975@yandex.co.il',
            recipient_list=[response.post.user.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})



class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 1
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = form.save()
        send_mail(
            subject='Новое объявление',
            message=f'Вы получили новое объявление: {response.content_text}',
            from_email='vitalivoloshin1975@yandex.co.il',
            recipient_list=[response.user.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('board:post-detail', kwargs={'pk': self.object.pk})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'board/post_delete.html'
    success_url = reverse_lazy('board:post-list')
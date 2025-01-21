from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from .filters import PostFilter
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.mail import send_mail


class UserCommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'board/user_comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post__user=self.request.user)


class CommentAcceptView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'board/comment_accept.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.object.post.id
        return context

    def form_valid(self, form):
        form.instance.accepted = True
        response = form.save()
        send_mail(
            subject='Ваш отклик был принят',
            message=f'Ваш отклик на объявление "{response.post.title}" был принят.',
            from_email='vitalivoloshin1975@yandex.co.il',
            recipient_list=[response.user.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('board:user-responses')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
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
        kwargs['post_id'] = self.kwargs.get('pk')  # Передаем post_id в форму
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs.get('pk')
        response = form.save()
        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'Вы получили новый отклик: {response.content}',
            from_email='vitalivoloshin1975@yandex.co.il',
            recipient_list=[response.post.user.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('board:post-detail', kwargs={'pk': self.object.post.pk})



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
            subject='Новый отклик на ваше объявление',
            message=f'Вы получили новый отклик: {response.content}',
            from_email='vitalivoloshin1975@yandex.co.il', recipient_list=[response.post.user.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


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
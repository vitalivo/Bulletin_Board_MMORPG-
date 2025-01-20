from django.urls import reverse_lazy
from datetime import datetime
from .filters import PostFilter
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .forms import PostForm


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


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'board/post_delete.html'
    success_url = reverse_lazy('board:post-list')
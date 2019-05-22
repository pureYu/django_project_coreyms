from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView
    , DetailView
    , CreateView
    , UpdateView
    , DeleteView
)
from .models import Post

# Create your views here.
def home(request):                 # FUNCTION VIEWS
    context = {
        'posts': Post.objects.all()
        , 'title': 'home'
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):     # CLASS BASED VIEW
    model = Post
    template_name = 'blog/home.html'  # instead of <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # '-' = desc
    paginate_by = 5


class UserPostListView(ListView):     # CLASS BASED VIEW
    model = Post
    template_name = 'blog/user_posts.html'  # instead of <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # '-' = desc
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):     # CLASS BASED VIEW
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):     # CLASS BASED VIEW
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):     # CLASS BASED VIEW
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):     # CLASS BASED VIEW
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blog/about.html', { 'title': 'About' })











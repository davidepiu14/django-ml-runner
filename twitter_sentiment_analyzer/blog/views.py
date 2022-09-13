import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


CSV_POLARITY_PATH = "/home/davide/code/personal/django_sentiment_analysis/twitter_sentiment_analyzer/sentiment/media_polarity.csv"
CSV_PIE_PATH = "/home/davide/code/personal/django_sentiment_analysis/twitter_sentiment_analyzer/sentiment/data_for_pie.csv"

def home(request):
    """Home page function"""
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    """
    PostListView: It shows last 5 post
    """
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    """
    UserPostListView: Post filtered by user
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    PostCreateView: allows users to create new posts (authentication required)
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    PostUpdateView: it allows to edit title and content (login required)
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """è possibile modificare i post solo dagli autori del post stesso"""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """PostDeleteView: Posts can be deleted only from the author"""
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def dahsboard_sentiment(request):
    """
    function: import data from csv and it shows sentiment results in dashboard.html 
    @return: render template
    """
    df = pd.read_csv(CSV_POLARITY_PATH)  
    rs_pie = pd.read_csv(CSV_PIE_PATH)
    date=list(df['new_date_column'].values)
    table_content = df.to_html(index=None)
    table_content = table_content.replace(
        'class="dataframe"', 
        "class='table table-striped'"
    )
    
    return render(
        request, 
        'blog/dashboard.html', 
        context={
            'data': date,
            'Trump': list(df['trump'].values),
            'Biden': list(df['biden'].values),
            'table_data': table_content,
            'Trump_positivi': list(rs_pie['trump'])[2],
            'Trump_negativi': list(rs_pie['trump'])[0],
            'Trump_neutrali': list(rs_pie['trump'])[1],
            'Biden_positivi': list(rs_pie['biden'])[2],
            'Biden_negativi': list(rs_pie['biden'])[0],
            'Biden_neutrali': list(rs_pie['biden'])[1]
        }
    )
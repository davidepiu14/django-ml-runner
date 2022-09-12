import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    #view fornite da django
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Post

CSV_POLARITY_PATH = "miosito/sentiment/media_polarity.csv"

CSV_PIE_PATH = 'miosito/sentiment/data_for_pie.csv'


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
    success_url = '/'#url a cui si viene rimandati una volta cancellato il post
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
    
    df = pd.read_csv(CSV_POLARITY_PATH)  # read data
    date=list(df['new_date_column'].values)
    values_trump,values_biden = list(df['Donald Trump'].values),list(df['Joe Biden'].values)#valori di polarity dei due candidati
    table_content = df.to_html(index=None)
    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    table_content = table_content.replace('border="2"', "")
    rs_pie = pd.read_csv(CSV_PIE_PATH)
    pieTrump,pieBiden = list(rs_pie['trump']),list(rs_pie['biden'])
    Trump_neg,Trump_net,Trump_pos   = (pieTrump[0]),(pieTrump[1]),(pieTrump[2])#Trump neg,pos,neutr percentage
    Biden_neg,Biden_net,Biden_pos = (pieBiden[0]),(pieBiden[1]),(pieBiden[2])#Biden tweet neg,pos,neutr percentage
    context = {
        'data': date,
        'Trump': values_trump,
        'Biden': values_biden,
        'table_data': table_content,
        'Trump_positivi':Trump_pos,
        'Trump_negativi':Trump_neg,
        'Trump_neutrali':Trump_net,
        'Biden_positivi':Biden_pos,
        'Biden_negativi':Biden_neg,
        'Biden_neutrali':Biden_net
    }

    return render(request, 'blog/dashboard.html', context=context)#inoltra request ad un template a cui verrano passati dei dati
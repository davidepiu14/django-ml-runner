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


def home(request):
    """nella pagina home.html vengono mostrati tutti i Post"""
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    """Post ordinati in base alla data di creazione, vengono mostrati 5 post per pagina"""
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    """mostra la lista dei post filtrato per utente"""
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
    """Permette di creare un Post, richiede che l'utente sia loggato"""
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Per modificare il Post è sempre necessario essere loggati, si possono modificare i campi
    relativi al titolo ed al contenuto"""
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
    """cancellazione del post permessa anche in questo caso solo all'autore del post in questione"""
    model = Post
    success_url = '/'#url a cui si viene rimandati una volta cancellato il post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def dahsboard_sentiment(request):
    """ import dataset csv per visualizzare i dati con HighCharts ed inoltrare i dati al template dashboard.html """
    # read data
    df = pd.read_csv("/home/davide/Scrivania/DAVIDE_PIU_WAAT_00106/00106_piu/miosito/sentiment/data/media_polarity.csv")
    date=list(df['new_date_column'].values)

    values_trump,values_biden = list(df['Donald Trump'].values),list(df['Joe Biden'].values)#qui sono presenti i valori di polarity dei due candidati

    # """table_content verrà utilizzata per la crezione di una tabella nella pagina della dashboard"""
    table_content = df.to_html(index=None)
    table_content = table_content.replace('class="dataframe"', "class='table table-striped'")
    table_content = table_content.replace('border="2"', "")

    rs_pie = pd.read_csv("/home/davide/Scrivania/DAVIDE_PIU_WAAT_00106/00106_piu/miosito/sentiment/data/data_for_pie.csv")#dataframe per la creazione dei dount charts

    pieTrump,pieBiden = list(rs_pie['trump']),list(rs_pie['biden'])


    Trump_neg,Trump_net,Trump_pos   = (pieTrump[0]),(pieTrump[1]),(pieTrump[2])#assegnate percentuali di tweet neg,pos,neutr relativi a Trump

    Biden_neg,Biden_net,Biden_pos = (pieBiden[0]),(pieBiden[1]),(pieBiden[2])#assegnate percentuali di tweet neg,pos,neutr relativi a Biden


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

    return render(request, 'blog/dashboard.html', context=context)#render inoltra una request ad un template a cui verrano passati dei dati
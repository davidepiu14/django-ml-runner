from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),#url home page, vengono mostrati tutti i post
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),#url utente, si viene rimandati in una pagina in cui vengono elencati tutti i post dell'utente in questione
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),#mostra dettagli post, pk è la chiave del post (intero)
    path('post/new/', PostCreateView.as_view(), name='post-create'),#path creazione di un nuovo post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),#path modifica dei post, pk è la chiave del post (intero)
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),#path per la cancellazione dei post. pk è la chiave del post (intero)
    path('dashboard/',views.dahsboard_sentiment, name='blog-dashboard'),#path della dashboard
]



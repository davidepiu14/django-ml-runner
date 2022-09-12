from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """viene passato uno dei modelli standard di Django"""
    title = models.CharField(max_length=100)#campo titolo di tipo char con max lunghezza 100
    content = models.TextField()#contenuto del post
    date_posted = models.DateTimeField(default=timezone.now)#data del post, automaticamente impostato alla data di creazione
    author = models.ForeignKey(User, on_delete=models.CASCADE)#quando viene cancellato l'autore vengono cancellati anche tutti i post da lui scritti

    def __str__(self):
        """il metodo __str__ restituisce il titolo del post"""
        return self.title

    def get_absolute_url(self):
        """django genera url"""
        return reverse('post-detail', kwargs={'pk': self.pk})

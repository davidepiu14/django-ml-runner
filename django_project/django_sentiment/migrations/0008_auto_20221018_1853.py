# Generated by Django 3.0.8 on 2022-10-18 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_sentiment', '0007_twitterpolarity_sign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='sentiment',
        ),
        migrations.AddField(
            model_name='tweet',
            name='polarity',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='tweet',
            name='sign',
            field=models.CharField(default='neutral', max_length=100),
        ),
    ]

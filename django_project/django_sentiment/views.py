import imp
import pandas as pd
from django.http import HttpResponse
from django_sentiment.models import Tweet
from django.shortcuts import render, get_object_or_404
from django_sentiment.management.commands._private import TwitterScraper



# Create your views here.




    
def dahsboard_sentiment(request):
    """
    function: import data from csv and it shows sentiment results in dashboard.html 
    @return: render template
    """
    ts = TwitterScraper()
    tweets = Tweet.objects.all().values('name','text','sign','polarity','location','verified','retweet','date','account','candidate') 
    df = pd.DataFrame(tweets)
    date = list(df['date'].values)
    df_test = ts.compute_time_series_tweets()
    print(df_test)
    print("*"*72)
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
            'Trump': list(df[df['candidate'] == 'trump'].values),
            'Biden': list(df[df['candidate'] == 'biden'].values),
            'table_data': table_content,

            'Trump_positivi': list(rs_pie['trump'])[2],
            'Trump_negativi': list(rs_pie['trump'])[0],
            'Trump_neutrali': list(rs_pie['trump'])[1],
            'Biden_positivi': list(rs_pie['biden'])[2],
            'Biden_negativi': list(rs_pie['biden'])[0],
            'Biden_neutrali': list(rs_pie['biden'])[1]
        }
    )

import imp
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django_sentiment.models import Tweet, TwitterPolarity
from django.shortcuts import render, get_object_or_404
from django_sentiment.management.commands._private import TwitterScraper



# Create your views here.




    
def dahsboard_sentiment(request):
    """
    function: import data from csv and it shows sentiment results in dashboard.html 
    @return: render template
    """
    ts = TwitterScraper()
    tweets = TwitterPolarity.objects.all().values('polarity','date','account','sign') 
    df = pd.DataFrame(tweets)
    date = list(df['date'].values)
    g = df.groupby(["account", "date"])
    daily_averages = g.aggregate({"polarity":np.mean})
    daily_averages=pd.DataFrame(daily_averages).reset_index()
    df_polarity = df.pivot(columns=['date','account'], values='polarity').reset_index()
    print(df_polarity)
    print("*"*100)
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
            'Trump': list(df[df['account'] == 'trump'].values),
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

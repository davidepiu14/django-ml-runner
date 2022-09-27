import imp
import pandas as pd
from django.http import HttpResponse
from django_sentiment.models import Tweet
# Create your views here.




    
def dahsboard_sentiment(request):
    """
    function: import data from csv and it shows sentiment results in dashboard.html 
    @return: render template
    """
    tweets = Tweet.objects.all()
    df = pd.DataFrame(tweets.values())
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

import re

def clean_text(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(https?\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    '''
    Comput sentiment with TextBlog
    @return: polarity
    '''
    text = clean_text(tweet)
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return {'sign': 'positive', 'polarity': analysis.sentiment.polarity}
    elif analysis.sentiment.polarity == 0:
        return {'sign': 'neutral', 'polarity': analysis.sentiment.polarity}
    else:
        return {'sign': 'negative', 'polarity': analysis.sentiment.polarity}


def get_tweets_sentiment(query, count=10):
    """
    Return tweet sentiment given a query, it return 10 tweets per page, 
    a mix beetween most populars and recents tweets
    @return: 
    """
    tweets_list = []
    try:
        fetched_tweets = tweepy.Cursor(
            twitterAPI.search_tweets, q=query, lang="en", tweet_mode='extended').items(count)

        for tweet in fetched_tweets:
            parsed_tweet = {
                'text': tweet.full_text,
                'name': tweet.user.name,
                'location': tweet.user.location,
                'verified': tweet.user.verified,
                'retweet': tweet.retweet_count,
                'date_tweet': tweet.created_at,
                'sentiment': get_tweet_sentiment(tweet.full_text)
            }
            print(tweet.full_text)
            if tweet.retweet_count > 0:
                if parsed_tweet['text'] not in tweets_list:
                    tweets_list.append(parsed_tweet)
            else:
                tweets_list.append(parsed_tweet)

        return tweets_list
    except Exception as e:
        print("Error : %s" % str(e))


def dump_tweets(query, count):
    """
    get tweets sentiment and save tweet result inside a csv file
    @return: file
    """
    tweets = get_tweets_sentiment(
        query=query,
        count=count
    )
    file_path = "tweets_%s.csv" % query.replace(' ', '_')
    with open(file_path, 'a', encoding="utf8") as file:
        csv_writer = csv.DictWriter(
            file,  
            quotechar='"',
            fieldnames=[
                'text', 
                'sentiment', 
                'name', 
                'location',
                'verified', 
                'retweet', 
                'date_tweet', 
                'candidate'
            ])
        csv_writer.writeheader()
        for tweet in tweets:
            csv_writer.writerow(tweet)
    
    return file_path
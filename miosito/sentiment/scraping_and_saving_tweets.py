import csv
import re
import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler

"""importo le credenziali dal file credentials.py e utilizzo tweepy per accedere all'API di twitter"""
from credentials import TWITTER_ACCESS_TOKEN, \
    TWITTER_CONSUMER_SECRET, \
    TWITTER_ACCESS_TOKEN_SECRET, \
    TWITTER_CONSUMER_KEY
auth = OAuthHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET
)

auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitterAPI = tweepy.API(auth)


def clean_text(tweet):
    """funzione che tramite le regular expression rimuove i pattern all'iinterno delle parentesi"""

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(https?\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    '''
    Calcola la sentiment analysis dei tweet utilzzando la libreria TextBlog, ad ogni testo dei tweet viene
    applicata la funzione clean_text()
    '''
    text = clean_text(tweet)
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return {'sign':'positive','polarity':analysis.sentiment.polarity}#se polarity>0 restituisce sign = 'positive'
    elif analysis.sentiment.polarity == 0:
        return {'sign':'neutral','polarity':analysis.sentiment.polarity}#se polarity=0 resituisce sign = 'neutral'
    else:
        return {'sign':'negative','polarity':analysis.sentiment.polarity}#altrimente restituisce sign = 'negative'


def get_tweets_sentiment(query, count=10):
    '''
    Data una specifica query restituisce la sentiment del tweet
    '''
    tweets = []
    try:
        """#si richama l'API per ottenere i tweet, vengono solamente selezionati i tweet in lingua inglese, 
        dato che count=10 vengono restituiti 10 tweet per pagina, non viene specificato se scaricare solo i più famosi 
        o più i più recenti, di default viene preso un mix dei due
        """
        fetched_tweets = tweepy.Cursor(twitterAPI.search, q=query,lang="en",tweet_mode='extended').items(count)
        """parsing dei tweet, ogni tweet viene salvato i un dizionario che avrà le chiavi che vediamo sotto"""
        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.full_text#testo dei tweet
            parsed_tweet['name']=tweet.user.name#nome utente dell'autore dei tweet
            parsed_tweet['location']=tweet.user.location#locazione dell'autore
            parsed_tweet['verified']=tweet.user.verified#restituisce yes/no se l'autente è verificato o meno
            parsed_tweet['retweet']=tweet.retweet_count#quante volte è stato ritwittato il tweet
            parsed_tweet['date tweet']= tweet.created_at#data creazione del tweet, data in formato estero
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.full_text)#per ogni tweet richiama la funzione get_tweet_sentiment
            print(tweet.full_text)
            if tweet.retweet_count > 0:
                """aggiunge i tweet che sono hanno subito retweet solo se il testo non è presente tra i tweet salvati"""
                if parsed_tweet['text'] not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        return tweets#restituisce una lista di dizionari
    except Exception as e:
        print("Error : %s" % str(e))

def dump_tweets(query, count):
    """questa funzione richiama la funzione get_tweet_sentiment e salva i tweet all'interno di
    un file csv"""
    tweets = get_tweets_sentiment(query=query,
                                  count=count)
    file_path = "tweets_%s.csv" % query.replace(' ', '_')#il nome del file comprende le parole oggetto della query
    with open(file_path, 'a', encoding="utf8") as file:#'a' sta a significare che stiamo aggiungendo ad un file già presente e non stiamo sovrascrivendo
        """DictWriter assegna ad ogni riga un dizionario, e all'interno di 'fieldname' ci sono le etichette """
        csv_writer = csv.DictWriter(file,
                                    quotechar='"',
                                   fieldnames=['text', 'sentiment','name','location',
                                               'verified','retweet','date tweet','candidato'])
        csv_writer.writeheader()
        for tweet in tweets:
            csv_writer.writerow(tweet)
    return file_path





if __name__=="__main__":#con if __name__=="__main__": è possibile richiamare le funzioni anche in altri file
    dump_tweets("donald trump",1000)#salvare i tweet di trump
    dump_tweets("joe biden",1000)#salvare i tweet di biden
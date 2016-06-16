import markovify
import tweepy

from configobj import ConfigObj

with open("corpus.txt") as f:
    text = f.read()

markovText = markovify.Text(text)

config = ConfigObj("twitter.conf")

tw_con_key = config['consumer_key']
tw_con_secret = config['consumer_secret']
tw_key = config['key']
tw_secret = config['secret']
tw_auth = tweepy.OAuthHandler(tw_con_key, tw_con_secret)
tw_auth.set_access_token(tw_key, tw_secret)
tw = tweepy.API(tw_auth)

def post(count=1):
    if count == 1:
        tweet = markovText.make_short_sentence(140)
        tw.update_status(tweet)
    elif count > 1:
        for i in range(count):
            tweet = markovText.make_short_sentence(140)
            tw.update_status(tweet)

if __name__ == "__main__":
    post()

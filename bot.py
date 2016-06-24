import markovify
import mechanicalsoup
import os
import tweepy

from configobj import ConfigObj

config = ConfigObj("twitter.conf")
tw_con_key = config['consumer_key']
tw_con_secret = config['consumer_secret']
tw_key = config['key']
tw_secret = config['secret']
tw_auth = tweepy.OAuthHandler(tw_con_key, tw_con_secret)
tw_auth.set_access_token(tw_key, tw_secret)
tw = tweepy.API(tw_auth)


def build_corpus():
    br = mechanicalsoup.Browser(soup_config={'markup_type': 'lxml'})
    response = br.get('http://www.gamefaqs.com/games/rankings')

    systems = []
    for i in response.soup.find_all('a')[:26]:
        ref = i.get('href')
        if not ref.startswith('/games'):
            systems.append(i.get('href') + '/')

    systems = tuple(systems)
    topGames = []

    for each in response.soup.find_all('a'):
        ref = str(each.get('href'))
        if ref.startswith(systems):
            topGames.append("http://www.gamefaqs.com" + ref + "/faqs")

    guides = []
    for link in topGames:
        resp = br.get(link)
        faq = []
        for each in resp.soup.find_all('a'):
            if '/faqs/' in str(each.get('href')):
                faq.append("http://www.gamefaqs.com" + each.get('href'))
        try:
            for each in faq[:8]:
                guides.append(each)
        except:
            pass

    # Clearing out ASCII Art
    badText = [
        "-", "=", "+", "~", "@", "&", "*", "<", ">", "\\", "/", "#", "`",
        "|", "_", ":", "(", ")"
        ]

    cleanGuides = []

    for guide in guides:
        resp = br.get(guide)
        text = resp.soup.find_all(attrs={'class': 'ffaq'})
        for each in text:
            guideText = each.get_text()
            for ch in badText:
                guideText = guideText.replace(ch, " ")
            # Strips out non-ascii characters
            cleanText = ''.join([i if ord(i) < 128 else ' ' for i in guideText])
            cleanGuides.append(cleanText)

    with open("corpus.txt", "a") as myfile:
        for i in cleanGuides:
            myfile.write(i)


def post(count=1):
    with open("corpus.txt", "r") as f:
        text = f.read()

    markovText = markovify.Text(text)

    if count == 1:
        tweet = markovText.make_short_sentence(140)
        tw.update_status(tweet)
    elif count > 1:
        for i in range(count):
            tweet = markovText.make_short_sentence(140)
            tw.update_status(tweet)

if __name__ == "__main__":
    if "corpus.txt" not in os.listdir():
        build_corpus()
        post()
    else:
        post()

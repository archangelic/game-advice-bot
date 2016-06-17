import mechanicalsoup

br = mechanicalsoup.Browser()

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

for guide in guides:
    resp = br.get(guide)
    text = resp.soup.find_all(attrs={'class': 'ffaq'})
    for each in text:
        guideText = each.get_text()
        for ch in badText:
            guideText = guideText.replace(ch, " ")
        # Strips out non-ascii characters because they aren't really necessary
        cleanText = ''.join([i if ord(i) < 128 else ' ' for i in guideText])
        print(cleanText)

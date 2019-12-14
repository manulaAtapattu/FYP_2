import yake
from yake.highlight import TextHighlighter

def getKeywords(text):
    #text= '''Essentially Marvel's flagship TV show, Agents of S.H.I.E.L.D. launched in 2013 and has already been renewed for an (abbreviated) seventh season for 2019-2020. Clark Gregg starred as Agent Coulson, with a two-season-long plot exploring the mystery of just how Coulson was resurrected after his death in The Avengers. Little by little, though, Chloe Bennet has become the series star, S.H.I.E.L.D.'s very own superhero, an Inhuman with the potential to literally tear the Earth apart. The rest of the cast is stellar, and each character has the kind of nuance and depth that's only possible when an actor really inhabits their role. The show's greatest strength is the fact that it can essentially be anything it wants to be; S.H.I.E.L.D. can plunge into a supernatural thriller alongside a new version of Ghost Rider, or be trapped in a dystopian future timeline in a hard sci-fi plot. Over the years, it's developed a mythology all of its own, one that allows it to stand a little bit more separate to the movies nowadays.'''
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 5

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    output = []
    for key in keywords:
        output.append(key[0])
    # th = TextHighlighter(max_ngram_size = 3, highlight_pre = "<span class='my_class' >", highlight_post= "</span>")
    # th.highlight(text, keywords)
    #
    # for kw in keywords:
    #     print(kw)
    return output
#getKeywords(None)



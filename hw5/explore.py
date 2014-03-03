
from pattern.web import *
from pattern.en import *
from revisions import *


w = Wikipedia()

def grabarticle(articlename):
    #returns a list of strings corresponding to each section content
    article = w.search(articlename)
    artsec = article.sections
    art = [i.string[len(i.title):] for i in artsec[1:]]
    artfull = [artsec[0].string]
    artfull.extend(art)
    artstr = ' '.join(artfull)
    return artstr
    
def grabarticlelinkless(articlename):
    artstr = grabarticle(articlename)
    artstr = artstr[:artstr.index(" * ^")]
    print artstr
    return artstr

def sentimentreturn(articlename)
    art = grabarticle(articlename)
    g = get_page_content(art.title,"en")
    keys = sorted(g)
    lenkey = len(keys)/49
    keys = [j for j in keys if keys.index(j)%lenkey==0 or keys.index(j)==len(keys)-1]
    a = list()
    for i in keys:
        a.append((sentiment(g[i]['content']),i))
    print a
    return a

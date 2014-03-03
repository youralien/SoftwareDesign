
from pattern.web import *
from pattern.en import *


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

    
g = grabarticlelinkless('Japanese American Internment')
a=grabarticle('Japanese American Internment')
#print a
print sentiment(a)
print sentiment(g)
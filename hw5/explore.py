
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

def sentimentreturn(articlename):
    # art = w.search(articlename)
    g = get_page_content(articlename,"en")
    keys = sorted(g)
    lenkey = len(keys)/49
    # lenkey = 1
    keys = [j for j in keys if keys.index(j)%lenkey==0 or keys.index(j)==len(keys)-1]
    a = list()
    start_epoch = convert_datetime_to_epoch(convert_to_datetime(keys[0]))
    for i in keys:
        # get date as an epoch (seconds)
        date = int(convert_datetime_to_epoch(convert_to_datetime(i)) - start_epoch)
        # get length of article
        content_length = len(g[i]['content'])
        a.append((sentiment(g[i]['content']),date, content_length))
    return a



if __name__ == '__main__':
    print sentimentreturn('Olin College')


from pattern.web import *

w = Wikipedia()

def grabarticle(articlename):
    article = w.search(articlename)
    return article

print grabarticle('Olin College').sections

from pattern.web import *

w = Wikipedia()

def grabarticle(articlename):
    article = w.search('Olin College')
    return article

print grabarticle('Olin College').sections
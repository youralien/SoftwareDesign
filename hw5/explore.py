
from pattern.web import *
w = Wikipedia()
olin_article = w.search('Olin College')
print olin_article.sections

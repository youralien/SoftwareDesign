"""
Software Design Spring 2014
HW5 - Text Mining
Ryan Louie and Deniz Celik
#graded
"""

import matplotlib.pyplot as plt
from explore import *

def SentimentTimePlot(article_title):
	"""
	Makes a plot of sentiment of an entire article over time

	"""

	V = sentimentreturn(article_title)
	times = [v[1] for v in V]
	polarity = [v[0][0] for v in V]
	subjectivity = [v[0][1] for v in V]
	article_length = [v[2] for v in V]

	fig, ax1 = plt.subplots()
	ax1.plot(times, polarity)
	ax1.plot(times, subjectivity)
	ax1.set_xlabel('Time from First Edit of Article (seconds)')
	ax1.set_ylabel('Sentiment')
	for tl in ax1.get_yticklabels():
		tl.set_color('b')
	ax1.legend(['polarity', 'subjectivity'], loc=2)


	ax2 = ax1.twinx()
	ax2.plot(times, article_length,'r-')
	ax2.set_ylabel('Article Length')
	for tl in ax2.get_yticklabels():
		tl.set_color('r')

	plt.title('{} Sentiment Analysis History'.format(article_title))	
	ax2.legend(['article_length'], loc=4)
	plt.show()

def SentimentArticleLength(article_title):
	"""
	Makes a scatter plot of sentiment vs article length, where
	each point is a revision in the article's history 

	"""
	V = sentimentreturn(article_title)
	polarity = [v[0][0] for v in V]
	subjectivity = [v[0][1] for v in V]
	article_length = [v[2] for v in V]

	plt.subplot(211)
	plt.scatter(article_length, polarity)
	
	plt.subplot(212)
	plt.scatter(article_length, subjectivity)
	plt.show()



if __name__ == '__main__':
	articles = [
	"Franklin W. Olin College of Engineering",
	"Japanese American internment",
	]
	SentimentTimePlot(articles[0])
	# SentimentArticleLength('Franklin W. Olin College of Engineering')
	


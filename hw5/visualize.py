"""
Software Design Spring 2014
HW5 - Text Mining
Ryan Louie and Deniz Celik
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
	plt.figure
	plt.plot(times, polarity)
	plt.title('{} Sentiment Analysis History'.format(article_title))
	plt.xlabel('Time from First Edit of Article (seconds)')
	plt.ylabel('Sentiment')
	plt.plot(times, subjectivity)
	plt.legend(['polarity', 'subjectivity'], loc=2)
	plt.show()

if __name__ == '__main__':
	SentimentTimePlot('Franklin W. Olin College of Engineering')

	


"""
grid.py
author: rlouie
"""


def drawgrid(dim = 2):
	"""
	dim: dim x dim grid
	"""

	major = ('+ '+'- '*4)*dim+'+'
	minor = ('| '+'  '*4)*dim+'|'


	for i in range(dim):
		print major
		for i in range(4):
			print minor
	print major

def main():
	drawgrid(2)
	print "\n"
	drawgrid(4)

if __name__ == '__main__':
	main()


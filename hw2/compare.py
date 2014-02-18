"""
compare.py
author: rlouie
"""

def compare(x, y):
	if x > y:
		return 1
	elif x == y:
		return 0
	else: 
		return -1

def main():
	print compare(2,1)
	print compare(2,2)
	print compare(2,3)

if __name__ == '__main__':
	main()

'''
Excellent work. Having a main function seems a bit redundant
'''
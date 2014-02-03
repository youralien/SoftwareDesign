"""
fermat.py
author: rlouie
"""

def check_fermat(a, b, c, n):
	if (a**n + b**n == c**n and n > 2):
		print "Holy Shit! Fermat was wrong!"
	else:
		print "Fermat says 'Q', 'E', 'D'"

def user_fermat():
	a = int(raw_input("Type a value for a: \n"))
	b = int(raw_input("Type a value for b: \n"))
	c = int(raw_input("Type a value for c: \n"))
	n = int(raw_input("Type a value for n: \n"))
	check_fermat(a, b, c, n)

def main():
	check_fermat(3, 4, 5, 2)
	check_fermat(3, 4, 5, 3)
	user_fermat()

if __name__ == "__main__":
	main()
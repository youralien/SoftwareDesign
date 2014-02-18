"""
fermat.py
author: rlouie
"""

def check_fermat(a, b, c, n):
	if (a**n + b**n == c**n and n > 2): 		# more efficient conditional
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

'''
Excellet work!

While it doesn't matter until much much later in your
career, you could make your conditional more efficient
by changing it to:
if (n > 2 and a**n + b**n == c**n):

Currently, it checks for the mathematical equality 
before n > 2. So if n == 1, then it would still 
evaluate the math statement before realizing n < 2.
'''
from sympy import symbols
from numpy import array
ro = array([0, 0.4, 0, 0.6])

x = symbols('x')
for i in range(len(ro)):
	if i==0:
		y = ro[i]*x**i;
	else:
		y = y + ro[i]*x**i;


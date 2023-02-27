def date_convert(input):
	pass

def measure_convert(input,measuring):
	return str(float(input * measuring[1])) + ' ' + measuring[0]

def sign(birth):
	dd = birth[0] + (birth[1] * 31)
	return 0
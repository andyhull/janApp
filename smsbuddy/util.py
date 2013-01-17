import re

# Cleans phone numbers entered to compare against other entries. 
def cleanphone(phonenumber):

	# removing all but the numbers
	cleaned = re.sub("[^0-9]", "", phonenumber)
	if len(cleaned) == 10:
		yield cleaned
	elif len(cleaned) <= 10:
		# this would be invalid
	else:
		#also an invalid number


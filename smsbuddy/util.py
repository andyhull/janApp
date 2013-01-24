import re

# Cleans phone numbers entered to compare against other entries. 
def cleanphone(phonenumber):

	# removing all but the numbers
	cleaned = re.sub("[^0-9]", "", phonenumber)
	if len(cleaned) == 10:
		cleaned = '+1'+cleaned
		return cleaned
	else:
		# generic response if the number is not valid
		return "-1"


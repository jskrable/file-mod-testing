import os, sys, json

def modFile(infile):

	# append _mod to input filename
	outfile = infile[:infile.index('.')] + '_mod' + infile[infile.index('.'):]

	# read infile data 
	with open(infile) as f:
		print('Reading file...')
		data = json.load(f)

	print('Applying modifications...')
	# iterate over data in file
	for i in range(len(data)):

		student = data[i]['applicant']
		app = data[i]['application']

		# change jan birthdays to march
		if student['birthDate'][4:6] == '01':
			student['birthDate'] = student['birthDate'][:4] + '03' + student['birthDate'][6:]

		# change waived fees to paid
		if app['applicationFeeExceptCd'] == '4':
			app['applicationFeeExceptCd'] = 'P'
			app['applicationFeeExcept'] = 'PAID'

		# flip housing options
		if app['housingOption'] == 'Commuter':
			app['housingOption'] = 'Resident'
		else :
			app['housingOption'] = 'Commuter'


	# write output file
	with open(outfile, 'w') as f:
		print('Writing modified file...')
		json.dump(data, f, indent = 2) 
		print('File successfully modified, ' + outfile)

# get input file from arg
infile = str(sys.argv[1])

try:
	# check input file 
	os.path.exists(infile)
	print('Good input file, continuing...')
	# execute mod script
	modFile(infile)

except IOError:
	print('An error occured while reading the file.')
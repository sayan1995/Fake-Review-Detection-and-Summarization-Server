import re
import os
import json

with open('../datasets/Cell_Phones_and_Accessories_5.json', 'r') as f:
	json_data = f.read()
	list=re.findall(r'(\{.*})',json_data)
	for i in list:
		data = json.loads(i)
		filename = '../datasets/CellPhones1/'+data['asin']+'.txt'
		if os.path.exists(filename):
			append_write = 'a' # append if already exists
			ff = open(filename,append_write)
			helpfulness = float(data['helpful'][0]/data['helpful'][1]) if data['helpful'][1] else 0
			ff.write("helpful"+":"+str(helpfulness)+".")
			ff.write("\n")
			ff.write("score"+":"+str(data['overall'])+".")
			ff.write("\n")
			ff.write("reviewerID"+":"+data['reviewerID']+".")
			ff.write("\n")
			ff.write(data['reviewText'])
			ff.write("\n\n")
		else:
			append_write = 'w' # make a new file if not
			ff = open(filename,append_write)
			helpfulness = float(data['helpful'][0]/data['helpful'][1]) if data['helpful'][1] else 0
			ff.write("helpful"+":"+str(helpfulness)+".")
			ff.write("\n")
			ff.write("score"+":"+str(data['overall'])+".")
			ff.write("\n")
			ff.write("reviewerID"+":"+data['reviewerID']+".")
			ff.write("\n")
			ff.write(data['reviewText'])
			ff.write("\n\n")

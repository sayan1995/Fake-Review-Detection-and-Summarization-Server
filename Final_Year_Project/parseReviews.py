import re
import os
import json
import gzip
import pickle

@profile
def parse(path):
	g = gzip.open(path, 'r')
	brand_reviews = {}
	reviewcount = 0
	for l in g:
		if(reviewcount <= 40000):
			json_data = json.dumps(eval(l))
			data = re.match(r'(\{.*})',json_data)
			json_obj = json.loads(data.group())
			obj = {"helpful":0.0,"score":0.0,"reviewerID":"","review":""}
			helpfulness = float(json_obj['helpful'][0]/json_obj['helpful'][1]) if json_obj['helpful'][1] else 0
			if "overall" in json_obj and "reviewerID" in json_obj and "reviewText" in json_obj:
				obj["helpful"] = helpfulness
				obj["score"] = json_obj["overall"]
				obj["reviewerID"] = json_obj["reviewerID"]
				obj["review"] = json_obj["reviewText"]
				if json_obj["asin"] not in brand_reviews:
					brand_reviews[json_obj["asin"]] = []
				brand_reviews[json_obj["asin"]].append(obj)
				#yield json_obj["asin"]+"|"+json_obj["brand"]+"|"+json_obj["title"]
			reviewcount+=1
		else:
			break

<<<<<<< HEAD
	filehandler = open("../datasets/movies&tv.pickle","wb")
	pickle.dump(brand_reviews,filehandler)	
parse("../datasets/Gzips/movies&tv.json.gz")
=======
	filehandler = open("../datasets/cellphones.pickle","wb")
	pickle.dump(brand_reviews,filehandler)	
parse("../datasets/Gzips/cellphones.json.gz")
>>>>>>> 9391fcbd2c85c5808aaea53b20cf39fecc5707fa
		


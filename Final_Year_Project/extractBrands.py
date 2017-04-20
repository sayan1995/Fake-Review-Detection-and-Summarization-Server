import re
import os
import json
import gzip
import pickle
import os.path

def parse(path):
	g = gzip.open(path, 'r')
	brands = {}
	brands_reviews = pickle.load( open( "../datasets/electronics.pickle", "rb" ) )
	for l in g:
		json_data = json.dumps(eval(l))
		data = re.match(r'(\{.*})',json_data)
		json_obj = json.loads(data.group())
		prod = {}
		if "brand" in json_obj and json_obj["brand"]!="" and "title" in json_obj and json_obj["asin"] in brands_reviews.keys():
			prod[json_obj["title"]] = json_obj["asin"]
			if json_obj["brand"] not in brands:
				brands[json_obj["brand"]] = []
			brands[json_obj["brand"]].append(prod)
			#yield json_obj["asin"]+"|"+json_obj["brand"]+"|"+json_obj["title"]

	filehandler = open("../datasets/Brands/electronics.pickle","wb")
	pickle.dump(brands,filehandler)		
			
parse("../datasets/Brands/meta_Electronics.json.gz")



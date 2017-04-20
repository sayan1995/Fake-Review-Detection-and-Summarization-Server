import os
import re
import json
import nltk
import math
import gzip
import time
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs={}
vocabulary = []
reviewList = []
stopwords = nltk.corpus.stopwords.words()
tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)

def analyze():
	documents=[]
	for i in docs:
		documents.append(docs[i]['text'])
	tfidf_vectorizer = TfidfVectorizer()
	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
	m,n = tfidf_matrix.shape
	doneflag=[0 for i in range(m)]
	reviewer = {}
	for i in range(m-1):
		cos_sim = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix)
		for j in range(len(cos_sim[0])):
			if cos_sim[0][j] > 0.75 and i!=j and docs[i]['reviewerID']==docs[j]['reviewerID'] and not doneflag[i] and not doneflag[j]:
				doneflag[i] = doneflag[j] = 1
				print docs[i]['asin']
				print docs[i]['text']
				print "\nis similar to\n"
				print docs[j]['asin']
				print docs[j]['text']
				print"\n"

def parse(domain):
	g = gzip.open('../datasets/Gzips/'+domain.lower()+'.json.gz', 'r')
	index = 0
	for l in g:
		#t0 = time.time()
		if index<=5000:
			json_data = json.dumps(eval(l))
			json_obj = re.match(r'(\{.*})',json_data)
			data = json.loads(json_obj.group())
			docs[index] = {'freq': {}, 'tf': {}, 'idf': {},
					'tf-idf': {}, 'tokens': [], 'reviewerID':"",'text':"",'asin':""}
			docs[index]["reviewerID"] = data["reviewerID"]
			docs[index]["text"] = data["reviewText"]
			docs[index]["asin"] = data["asin"]
			#t1 = time.time()
			#print t1-t0
			index+=1
		else:
			break
	analyze()

				

		

import re
import os
import time
import gzip
import nltk
import json
import pandas
import pickle
import string
import collections
from nltk import tokenize
from textblob import TextBlob
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def parse(readpath,writepath,domain):
	brands_reviews = pickle.load( open( "../datasets/"+domain.lower()+".pickle", "rb" ) )
	docs={}
	vocabulary = []
	reviewList = []
	stopwords = nltk.corpus.stopwords.words()
	tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)
	g = gzip.open(readpath, 'r')

	fwrite = open(writepath,'w')
	reviewmap = {}
	reviewcount=0
	for l in g:
		#t0 = time.time()
		if reviewcount <= 10000:
			json_data = json.dumps(eval(l))
			json_obj = re.match(r'(\{.*})',json_data)
			data = json.loads(json_obj.group())
			#t1 = time.time()
			#print "1",t1-t0
			#if reviewcount <= 2000:
			#reviewcount+=1
			rating = 0
			#data = json.loads(i)
			review = data["reviewText"]
			asin = data["asin"]
			#t0 = time.time()
			review_data = brands_reviews[asin]
			#t1 = time.time()
			#print "2",t1-t0
			#t0 = time.time()
			for i in review_data:
				rating+=float(i["score"])
			average_rating = rating/float(len(review_data))
			#t1 = time.time()	
			#print "3",t1-t0
			#t0 = time.time()
			#text = nltk.word_tokenize(review)
			#pos_tagged = nltk.pos_tag(text)
			#counts = Counter(tag for word,tag in pos_tagged)
			#t1 = time.time()
			#print "4",t1-t0
			#t0 = time.time()
			caps = len(filter(lambda x: x in string.uppercase, review))
			#t1 = time.time()
			#print "5",t1-t0
			analyze_text = TextBlob(review)
			review_status = [0 for i in range(6)]
			review_data = [0 for i in range(6)]
			if len(review)!=0:# and abs(average_rating-float(data["overall"]))>2:
				c = Counter(c for c in review if c in ["?","!"])
				review_data[0] = abs(float(data["overall"])-average_rating)
				review_data[1] = analyze_text.subjectivity
				review_data[2] = float(caps)/len(review)
				review_data[3] = float(c["?"]+c["!"])/len(review)
				review_data[4] = float(len(analyze_text.words))/1000
				helpfulness = float(data['helpful'][0])/float(data['helpful'][1]) if data['helpful'][1] else 0
				review_data[5] = helpfulness						
				fwrite.write(data["reviewerID"]+","+data["asin"]+","+str(review_data[0])+","+str(review_data[1])+","+str(review_data[2])+","+str(review_data[3])+","+str(review_data[4])+","+str(review_data[5])+"\n")
			reviewcount+=1
		else:
			break	

def predict(ch,domain):
	brands_reviews = pickle.load( open( "../datasets/"+domain.lower()+".pickle", "rb" ) )
	newpath = '../datasets/ML/'+domain+'_review.csv'
	cols = pandas.read_csv(newpath).columns
	X_validation = pandas.read_csv(newpath,usecols=cols[2:8])
	scoring = 'accuracy'

	if ch==1:	
		knn = pickle.load(open( "../datasets/ML/Models/knn_review.p", "rb" ))
		predictions = knn.predict(X_validation)
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_review_label.csv', 'w') as fout:
			index = 0
			#fout.write("ReviewerID,Negative,Neutral,Positive,Helpfulness,Burst,Count,Label\n")
			for line in iter(fin.readline, ''):
		            arr=line.split(",")
			    reviewerID=arr[0]
			    brandID=arr[1]
			    for i in brands_reviews[brandID]:
				if i["reviewerID"]==reviewerID:
					review = i["review"]	
			    fout.write(line.replace('\n', ',' + str(predictions[index]) + ',' + review+'\n'))
			    index += 1

	elif ch==2:
		svc = pickle.load(open( "../datasets/ML/Models/svc_review.p", "rb" ))
		predictions = svc.predict(X_validation)
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_review_label.csv', 'w') as fout:
			index = 0
			#fout.write("ReviewerID,Negative,Neutral,Positive,Helpfulness,Burst,Count,Label\n")
			for line in iter(fin.readline, ''):
		            arr=line.split(",")
			    reviewerID=arr[0]
			    brandID=arr[1]
			    for i in brands_reviews[brandID]:
				if i["reviewerID"]==reviewerID:
					review = i["review"]	
			    fout.write(line.replace('\n', ',' + str(predictions[index]) + ',' + review+'\n'))
			    index += 1

	elif ch==3:
		cart = pickle.load(open( "../datasets/ML/Models/cart_review.p", "rb" ))
		predictions = cart.predict(X_validation)	
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_review_label.csv', 'w') as fout:
			index = 0
			header = fin.readline()
			#fout.write("ReviewerID,Negative,Neutral,Positive,Helpfulness,Burst,Count,Label\n")
			for line in iter(fin.readline, ''):
		            arr=line.split(",")
			    reviewerID=arr[0]
			    brandID=arr[1]
			    for i in brands_reviews[brandID]:
				if i["reviewerID"]==reviewerID:
					review = i["review"]	
			    fout.write(line.replace('\n', ',' + str(predictions[index]) + ',' + review+'\n'))
			    index += 1

	elif ch==4:
		nb = pickle.load(open( "../datasets/ML/Models/nb_review.p", "rb" ))
		predictions = nb.predict(X_validation)	
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_review_label.csv', 'w') as fout:
			index = 0
			#fout.write("ReviewerID,BrandId,Negative,Neutral,Positive,Helpfulness,Burst,Count,Label\n")
			for line in iter(fin.readline, ''):
		            arr=line.split(",")
			    reviewerID=arr[0]
			    brandID=arr[1]
			    for i in brands_reviews[brandID]:
				if i["reviewerID"]==reviewerID:
					review = i["review"]	
			    fout.write(line.replace('\n', ',' + str(predictions[index]) + ',' + review+'\n'))
			    index += 1

	elif ch==5:
		lda = pickle.load(open( "../datasets/ML/Models/lda_review.p", "rb" ))
		predictions = lda.predict(X_validation)	
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_review_label.csv', 'w') as fout:
			index = 0
			#fout.write("ReviewerID,Negative,Neutral,Positive,Helpfulness,Burst,Count,Label\n")
			for line in iter(fin.readline, ''):
		            arr=line.split(",")
			    reviewerID=arr[0]
			    brandID=arr[1]
			    for i in brands_reviews[brandID]:
				if i["reviewerID"]==reviewerID:
					review = i["review"]	
			    fout.write(line.replace('\n', ',' + str(predictions[index]) + ',' + review+'\n'))
			    index += 1

	

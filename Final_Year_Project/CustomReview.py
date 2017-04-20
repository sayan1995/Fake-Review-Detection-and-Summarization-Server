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
import numpy as np
from nltk import tokenize
from textblob import TextBlob
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

def parse_custom(review, domain="cellphones"):
	brands = pickle.load( open( "../datasets/Brands/"+domain.lower()+".pickle", "rb" ) )
	brandslist = []
	for i in brands.keys():
		brand_words = i.split()
		brandslist+=brand_words
		for j in brands[i]:
			title_words = j.items()[0][0].split()			
			brandslist+=title_words
	brandslist = set(brandslist)
	vocabulary = []
	reviewList = []
	stopwords = nltk.corpus.stopwords.words()
	tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)
	text = nltk.word_tokenize(review)
	cnt = 0
	for i in text:
		if i in brandslist:
			cnt+=1
	pos_tagged = nltk.pos_tag(text)
	analyze_text = TextBlob(review)
	counts = Counter(tag for word,tag in pos_tagged)
	caps = len(filter(lambda x: x in string.uppercase, review))			
	review_status = [0 for i in range(6)]
	review_data = [0 for i in range(6)]
	if len(review)!=0:
		c = Counter(c for c in review if c in ["?","!"])
		review_data[0] = float(counts['PRP$'])-float(counts['PRP'])
		review_data[1] = analyze_text.subjectivity
		review_data[2] = float(caps)/len(review)
		review_data[3] = float(c["?"]+c["!"])/len(review)
		review_data[4] = float(len(analyze_text.words))/1000
		review_data[5] = float(cnt)/float(len(analyze_text.words))
	if review_data[0]>0:
		review_status[0] = 1
	if review_data[1] < 0.5:
		review_status[1] = 1
	if review_data[2] >= 0.5:
		review_status[2] = 1
	if review_data[3] >=0.1:
		review_status[3] = 1
	if review_data[4] <= 0.135:
		review_status[4] = 1
	if review_data[5] >= 0.5 or review_data[5]<=0.1:
		review_status[5] = 1
	return review_status	

def parse(readpath = '../datasets/Gzips/cellphones.json.gz',writepath = '../datasets/ML/custom_review.csv', domain="cellphones"):
	brands_reviews = pickle.load( open( "../datasets/"+domain.lower()+".pickle", "rb" ) )
	docs={}
	brands = pickle.load( open( "../datasets/Brands/"+domain.lower()+".pickle", "rb" ) )
	brandslist = []
	for i in brands.keys():
		brand_words = i.split()
		brandslist+=brand_words
		for j in brands[i]:
			title_words = j.items()[0][0].split()			
			brandslist+=title_words
	brandslist = set(brandslist)
	vocabulary = []
	reviewList = []
	stopwords = nltk.corpus.stopwords.words()
	tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)
	g = gzip.open(readpath, 'r')
	fwrite = open(writepath,'w')
	reviewmap = {}
	reviewcount=0
	for l in g:
		if reviewcount <= 10000:
			cnt = 0
			json_data = json.dumps(eval(l))
			json_obj = re.match(r'(\{.*})',json_data)
			data = json.loads(json_obj.group())
			review = data["reviewText"]
			asin = data["asin"]
			review_data = brands_reviews[asin]
			text = nltk.word_tokenize(review)
			for i in text:
				if i in brandslist:
					cnt+=1
			pos_tagged = nltk.pos_tag(text)
			analyze_text = TextBlob(review)
			counts = Counter(tag for word,tag in pos_tagged)
			caps = len(filter(lambda x: x in string.uppercase, review))			
			review_status = [0 for i in range(6)]
			review_data = [0 for i in range(6)]
			if len(review)!=0:
				c = Counter(c for c in review if c in ["?","!"])
				review_data[0] = float(counts['PRP$'])-float(counts['PRP'])
				review_data[1] = analyze_text.subjectivity
				review_data[2] = float(caps)/len(review)
				review_data[3] = float(c["?"]+c["!"])/len(review)
				review_data[4] = float(len(analyze_text.words))/1000
				review_data[5] = float(cnt)/float(len(analyze_text.words))	
				if review_data[0]>0:
					review_status[0] = 1
				if review_data[1] < 0.5:
					review_status[1] = 1
				if review_data[2] >= 0.5:
					review_status[2] = 1
				if review_data[3] >=0.1:
					review_status[3] = 1
				if review_data[4] <= 0.135:
					review_status[4] = 1
				if review_data[5] >= 0.5 or review_data[5]<=0.1:
					review_status[5] = 1
				detection_counter=collections.Counter(review_status)
				if(detection_counter[1]>=3):
					label = "FAKE"
				else:
					label = "TRUTHFUL"					
				fwrite.write(str(review_data[0])+","+str(review_data[1])+","+str(review_data[2])+","+str(review_data[3])+","+str(review_data[4])+","+str(review_data[5])+","+label+"\n")
			reviewcount+=1
		else:
			break	

def predict(domain="cellphones"):
	brands_reviews = pickle.load( open( "../datasets/"+domain.lower()+".pickle", "rb" ) )
	newpath = '../datasets/ML/custom_review.csv'
	cols = pandas.read_csv(newpath, header = None).columns
	X = pandas.read_csv(newpath,header = None,usecols=cols[0:6])
	Y = np.array(pandas.read_csv(newpath, header = None,usecols=cols[6:7])).ravel()
	validation_size = 0.20
	seed = 7
	scoring = 'accuracy'
	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
	# Make predictions on validation dataset
	knn = KNeighborsClassifier()
	knn.fit(X_train, Y_train)
	pickle.dump( knn, open( "save.p", "wb" ) )
	predictions = knn.predict(X_validation)
	print(accuracy_score(Y_validation, predictions))
	print(confusion_matrix(Y_validation, predictions))
	print(classification_report(Y_validation, predictions))

'''	if ch==1:	
		knn = pickle.load(open( "../datasets/ML/Models/knn_custom_review.p", "rb" ))
		predictions = knn.predict(X_validation)
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_custom_review_label.csv', 'w') as fout:
			index = 0
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
		with open(newpath) as fin, open('../datasets/ML/'+domain+'_custom_review_label.csv', 'w') as fout:
			index = 0
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
			for line in iter(fin.readline, ''):
		            arr=line.split(",")
			    reviewerID=arr[0]
			    brandID=arr[1]
			    for i in brands_reviews[brandID]:
				if i["reviewerID"]==reviewerID:
					review = i["review"]	
			    fout.write(line.replace('\n', ',' + str(predictions[index]) + ',' + review+'\n'))
			    index += 1'''
def pred():
	knn = pickle.load(open( "save.p", "rb" ))
	X_validation = parse_custom("Iphone is a complete rip off")
	print X_validation
	predictions = knn.predict(X_validation)
	print predictions
pred()
#parse()

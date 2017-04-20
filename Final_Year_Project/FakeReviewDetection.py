import reviewer_ml_parse
import reviewer_ml_main
import review_ml_parse
import review_ml_main
import os.path
import cosine_similarity
import pandas as pd
import numpy as np
import re
import json
import gzip

print("1.CellPhones and Accessories")
print("2.Movies and TV shows")
print("3.Android Apps")
print("4.Clothes-and-Accessories")
print("5.Video Games")
print("6.Beauty Products")
print("7.Automotive")
print("8.Musical-Instruments")

print "Enter your choice"
dom_choice=int(raw_input())
domain_list=["CellPhones","Movies&TV","AndroidApps","Clothes&Acc","VideoGames","Beauty","Automotive","Musical-Instruments"]

print "1.Reviewer Based"
print "2.Review Based"
print "3.Cosine similarity"
print "Enter your choice"
choice=int(raw_input())

def reviewerBased(domain):
	if os.path.exists("../datasets/ML/"+domain.lower()+"_label.csv"):
		df = pd.read_csv("../datasets/ML/"+domain.lower()+"_label.csv")
		for j in df[df['Label'] == 'FAKE']["ReviewerID"].tolist():
			print j
			g = gzip.open('../datasets/Gzips/'+domain.lower()+'.json.gz', 'r')
			for l in g:
				json_data = json.dumps(eval(l))
				json_obj = re.match(r'(\{.*})',json_data)
				data = json.loads(json_obj.group())
				if data["reviewerID"]==j:
					print data["reviewText"]
					print ""
			print ""
	else:
		if not os.path.exists('../datasets/ML/'+domain.lower()+'.csv'):	
			reviewer_ml_parse.parse('../datasets/Gzips/'+domain.lower()+'.json.gz','../datasets/ML/'+domain.lower()+'.csv') 
		print "1. Use K-Means algorithm"
		print "2. Use Models"
		print "Enter your choice"
		algo = int(raw_input())
		if algo==1:
			reviewer_ml_main.evaluate(domain.lower(),'../datasets/ML/'+domain.lower()+'.csv')
		elif algo==2:
			print("1. K Nearest Neighbours")
			print("2. SVM")
			print("3. Decision Trees")
			print("4. Naive Bayes")
			print("5. Linear Discriminant Analysis")
			print("Choose classifier")
			cls = int(raw_input())
			reviewer_ml_main.predict(cls,domain.lower())
			if os.path.exists("../datasets/ML/"+domain.lower()+"_label.csv"):
				df = pd.read_csv("../datasets/ML/"+domain.lower()+"_label.csv")
				for j in df[df['Label'] == 'FAKE']["ReviewerID"].tolist():
					print j
					g = gzip.open('../datasets/Gzips/'+domain.lower()+'.json.gz', 'r')
					for l in g:
						json_data = json.dumps(eval(l))
						json_obj = re.match(r'(\{.*})',json_data)
						data = json.loads(json_obj.group())
						if data["reviewerID"]==j:
							print data["reviewText"]
							print ""
					print ""

def reviewBased(domain):
	if not os.path.exists('../datasets/ML/'+domain.lower()+'_review.csv'):
		review_ml_parse.parse('../datasets/Gzips/'+domain.lower()+'.json.gz','../datasets/ML/'+domain.lower()+'_review.csv',domain.lower())
	if not os.path.exists('../datasets/ML/'+domain.lower()+'_review_label.csv'):
		print("1. K Nearest Neighbours")
		print("2. SVM")
		print("3. Decision Trees")
		print("4. Naive Bayes")
		print("5. Linear Discriminant Analysis")
		print("Choose classifier")
		cls = int(raw_input())
		review_ml_parse.predict(cls,domain.lower())
	else:
		print "Exists"

if(dom_choice==1):
	domain=domain_list[0]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)

elif(dom_choice==2):
	domain=domain_list[1]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)

elif(dom_choice==3):
	domain=domain_list[2]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)

elif(dom_choice==4):
	domain=domain_list[3]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)	

elif(dom_choice==5):
	domain=domain_list[4]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)	

elif(dom_choice==6):
	domain=domain_list[5]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)	

elif(dom_choice==7):
	domain=domain_list[6]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)	

elif(dom_choice==8):
	domain=domain_list[7]
	if choice==1:
		reviewerBased(domain)
	elif choice==2:
		reviewBased(domain)
	elif(choice==3):
		cosine_similarity.parse(domain)

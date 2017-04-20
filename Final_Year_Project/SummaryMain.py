import re
import nltk
import pickle
import keywords
import TFIDFSummary
import TextRank
from time import sleep
from nltk.tokenize import RegexpTokenizer

def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
<<<<<<< HEAD
    return stop_words
=======
    return stop_words	
>>>>>>> 9391fcbd2c85c5808aaea53b20cf39fecc5707fa

def main(dom_choice,domain_list):
	if(dom_choice > len(domain_list)):
		print "Wrong choice"
		return "Wrong choice"
	domain=domain_list[dom_choice-1]
	f = open("../datasets/Brands/"+domain.lower()+".pickle",'rb')
	object_file = pickle.load(f)
	prodslist={}
	c=0;
	brandslist={}
	prodslist={}
	for brand in object_file.keys():
		#brand.append(line.split('|')[0])
		brandslist[c+1]=brand
		print str(c+1)+". "+brand+"\n"
		c+=1
<<<<<<< HEAD

=======
	
>>>>>>> 9391fcbd2c85c5808aaea53b20cf39fecc5707fa
	print "Enter your choice"
	ch=int(raw_input())
	#ch=ch-1
	selectedBrand = brandslist[ch]
	print selectedBrand
	c=0
	for prods in range(len(object_file[selectedBrand])):
		for prod in object_file[selectedBrand][prods].keys():
			prodslist[c+1]=object_file[selectedBrand][prods][prod]
			print str(c+1)+". "+prod+"\n"
		c+=1

	print "Enter your choice"
	ch=int(raw_input())
<<<<<<< HEAD
	#ch=ch-1
=======
	#ch=ch-1	
>>>>>>> 9391fcbd2c85c5808aaea53b20cf39fecc5707fa
	print "1.Summary using Text Rank"
	print "2.Summary using TF-IDF"
	print "Enter your choice"
	choice=int(raw_input())

	summary=""

	if choice==1:
		print "Do you want to enable debugging (Y/N)?"
		ch_debug=raw_input().lower()
		if ch_debug=="y" or ch_debug=="yes":
			rankedText = TextRank.summaryGen(prodslist[ch],domain,debugging=True)
		else:
<<<<<<< HEAD
			rankedText = TextRank.summaryGen(prodslist[ch],domain)


=======
			rankedText = TextRank.summaryGen(prodslist[ch],domain)	

	
>>>>>>> 9391fcbd2c85c5808aaea53b20cf39fecc5707fa
		f.close()
		sleep(3)
		#rankedText=rankedText[:len(rankedText)/3]

	if choice==2:
		print "Do you want to enable debugging (Y/N)?"
		ch_debug=raw_input().lower()
		print "Do you want to enter the token size (Y/N)?"
		ch_token=raw_input().lower()
		if ch_debug=="y" or ch_debug=="yes":
			if ch_token=="y" or ch_token=="yes":
				print "Enter token size"
				token=int(raw_input())
				rankedText=TFIDFSummary.summaryGen(prodslist[ch],domain,gram=token,debug=True)
			else:
				rankedText=TFIDFSummary.summaryGen(prodslist[ch],domain,debug=True)
		else:
			if ch_token=="y" or ch_token=="yes":
				print "Enter token size"
				token=int(raw_input())
				rankedText=TFIDFSummary.summaryGen(prodslist[ch],domain,gram=token)
			else:
				rankedText=TFIDFSummary.summaryGen(prodslist[ch],domain)

	keys=keywords.extract_keywords(domain,prodslist[ch])
	rankedSummary=""
	for i in range(len(rankedText)):
		rankedSummary+=rankedText[i]
	stopwords=load_stop_words("../stoplist.txt")
	tokenizer = RegexpTokenizer("[\w']+", flags=re.UNICODE)
	tokens = tokenizer.tokenize(rankedSummary)
	tokens = [token for token in tokens if token.lower() not in stopwords]
	precision = float(len(set(tokens).intersection(set(keys))))/float(len(tokens))
	recall = float(len(set(tokens).intersection(set(keys))))/float(len(keys))
	fmeasure = 2*(precision*recall)/(precision+recall)
	print "\n\n"
	print "Precision =",precision
	print "Recall =",recall
	print "F-Measure =",fmeasure

if __name__ == '__main__':
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

	main(dom_choice, domain_list)

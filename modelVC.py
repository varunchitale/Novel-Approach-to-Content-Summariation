import cosine
import nltk
import numpy as np
from threading import Thread
import threading

class summary:

	text=""
	n=0
	weightGraph=[]
	

	def buildGraph(self,sentences,i,tImpWord):
		j=0
		global n,weightGraph
		#print threading.currentThread()		
		for j in range (i+1,n):
			weightGraph[i][j]=cosine.cosineS(sentences[i],sentences[j])
			
		if tImpWord[i]:
			#print "Before adding " ,weightGraph[i][j]
			weightGraph[i][j] += 0.1*tImpWord[i]
			#print "After adding " ,weightGraph[i][j]	

		weightGraph[i][i]=0.0


	def summarize(self,text,reductionRatio,heavywords):
		global n,selectedSent
		
		sentences=text.split('.')
		#print len(text)
		
		#text1=text
		text1=text.replace('\"','')
		text1=text1.replace(',',' ')
		#text1=text1.replace('...','.')
		#text1=text1.replace('....','.')
		sentences1=text1.split('.')
		
		
		n=len(sentences)-1
		
		with open("stopWords.txt") as f:
		    stopWords=f.read().split()
		


		t=["" for i in range(n)]
		tImpWord=[0 for i in range(n)]

		heavywords=heavywords.split()
		
		for i in range(n):
			t[i]=sentences[i].split(" ")	
			sentences1[i]=' '.join(word for word in t[i] if word not in stopWords)+'.'		
			for word in heavywords:
				if word in t[i]:
					tImpWord[i] += 1
					#print tImpWord[i] 
					#print "heavy Word present, Added value to sent no: ",i
		
		#print "Sentences:\n"
		#print sentences
					
		global weightGraph
		weightGraph=[[0 for x in range(n)] for y in range(n)]

		tCount=[0 for i in range(0,n)]

		#Expoliting MultiThreading
		for i in range (0,n):
			#Sequential:
			#self.buildGraph(sentences,i,tImpWord)
			t=Thread(target=self.buildGraph, args=(sentences1,i,tImpWord,))
			t.start()
												
		t.join()

		#print "Matrix of weigh graph:\n"
		#print (np.matrix(weightGraph))
		
		gist=self.gist(weightGraph,sentences,reductionRatio)
		#print "Summary:\n" ,gist
		return gist

	def gist(self,weightGraph,sentences,reductionRatio):
		gist=""
		global n,selectedSent
		
		sum1=[0 for i in range(n)]
		selectedSent=[0 for i in range(n)]
		
		for i in range(0,n):
			for j in range(0,n):
				sum1[i]=sum1[i]+weightGraph[i][j]+weightGraph[j][i]
	
	
		#print "\n" ,np.matrix(sum1)
		rank=sorted(range(n),key=lambda x:sum1[x])[::-1]

		#print "\nRank array\n"
		#print rank

		i=0
		#print n*reductionRatio
		while i < n * reductionRatio:
			selectedSent[rank[i]]=1		
			i+=1
		
		
		for i in range(0,n):
			if selectedSent[i]==1:
				gist=gist+sentences[i]+"."
		
		#print "Selected sentences array:\n"
		#print np.matrix(selectedSent)
		return gist

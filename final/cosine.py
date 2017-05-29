import math
from scipy import spatial

def cosineS(text1,text2):
	value=0
	
#get word count
	t1=text1.lower().split(' ')
	t2=text2.lower().split(' ')	

	f1={}
	f2={}
	
	t=''
	t=t1+t2 #concatenate them together
	
#remove duplicate words
	for word in t2:
		if word in t1:
			t.remove(word)
	
	#compute vectors
	for i in t:
		if i in t1:
			f1[i]=1
		else:
			f1[i]=0	
		
	
	for i in t:
		if i in t2:
			f2[i]=1
		else:
			f2[i]=0	
	
		
#cosine =a.b/sqrt(ab)
	num=numerator(f1,f2,t)
	den=denominator(f1,f2)
	
#computing cosine similarity
	if den==0:
		return 0
	else:
		value=num/den

	return value

def numerator(f1,f2,t):
	num=0
	
	for i in t:
		if (f1[i]==1 and f2[i]==1):
			num+=1
	
	return num

def denominator(f1,f2):
	den1=0
	den2=0
	den=0
	
	
	for i in f1:
		den1+=(f1[i]**2)
	
	for i in f2:
		den2+=(f2[i]**2)
	
	
	den=den1*den2
	den=math.sqrt(den)
	return den
	

#value=cosineS(text1,text2)
#print value


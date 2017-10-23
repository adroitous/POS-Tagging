from collections import Counter, namedtuple
import math
import pprint
import nltk
import numpy as np
def tokenize_text(text):
	""" Converts a string to a list of tokens """
	text = text.split()
	word = []
	tag = []
	for element in text:	
		function = element.split('/')
		word.append(function[0])
		tag.append(function[1])
	word = list(filter(lambda x: x != '', word))
	return [word, tag]
	#print word
	#print tag


def tagTable(taglist, tagset, length):
	#initialize the tagtable
	tagTable = [[1 for x in range(length+2)] for y in range(length+2)]
	temp = tagset
	for i in range(length): 
		element = tagset.pop()
		tagTable[0][i+1] = element
		tagTable[i+1][0] = element
	tagTable[0][0] = "empty"
	tagTable[0][length+1] = "q_0"
	tagTable[length+1][0] = "q_f"
	#print len(taglist)
	for i in range(len(taglist)-1):
		for j in range(length+2):
			if taglist[i] == tagTable[0][j]: 
				#print tagTable[0][j]
				for h in range(length+2):
					if tagTable[h][0] == taglist[i+1]: 
						#print "h "
						#print h						
						#print "j"
						#print j
						#print tagTable[h][j]
						tagTable[h][j] += 1
	print(np.matrix(tagTable))
	return tagTable

def wordTable(wordlist, wordset, wordlength, taglist, tagset, taglength):
	Table = [[1 for x in range(taglength+1)] for y in range(wordlength+1)]
	temptag = tagset
	tempword = wordset
	for i in range(taglength): 
		Table[0][i+1] = temptag.pop()
	for i in range(wordlength):
		Table[i+1][0] = tempword.pop()
	Table[0][0] = "empty"
	#print wordlength
	#print taglength
	dlist = []
	for f in range(len(wordlist)):
		dlist.append((wordlist[f],taglist[f]))
	for i in range(taglength):		
		for j in range(wordlength):
			for k in range(len(dlist)):
				if Table[0][i+1] == dlist[k][1]:
					if Table[j+1][0] == dlist[k][0]:
						Table[j+1][i+1] += 1
	print(np.matrix(Table))
	return Table

def TableProb(wordTable):
	probabilityTable = wordTable
	probabilityTableData =  [row[1:] for row in probabilityTable[1:]]
	temp = probabilityTable
	col_totals = [sum(x) for x in zip(*probabilityTableData)]
	for i in range(len(probabilityTableData[0])):
		for j in range(len(map(len, probabilityTableData))):
			temp[j+1][i+1] = '%.3f'%(float(probabilityTableData[j][i])/float(col_totals[i-1]))
	print(np.matrix(temp))
	return temp

#def lookProb():


def calcProb(textprocessed, tagprocessed, tagTable, wordTable):
	count = 1
	
	for i in range(len(textprocessed)):
		count*=lookProb(wordTable, tagprocessed[i], textprocessed[i])
	for i in range(len(tagprocessed)-1):
		#print lookProb(tagTable, tagprocessed[i], tagprocessed[i+1])
		count*=lookProb(tagTable, tagprocessed[i], tagprocessed[i+1])
	print lookProb(tagTable, tagprocessed[-1], 'q_f')
	count*= lookProb(tagTable, tagprocessed[-1], 'q_f')
	return count


def lookProb(ptable, given, actual):
	for i in range(len(ptable[0])-1):
		for j in range(len(map(len, ptable))-1):
			if ptable[j+1][0] == actual:
				if ptable[0][i+1] == given:
					#print ptable[j+1][i+1]
					return float(ptable[j+1][i+1])
	print "should not happen"


def Viterbi(text, tagTable, wordTable):
	tags = []
	for j in range(len(tagTable)-2):
		#print tagTable[0][j+1]
		tags.append(tagTable[0][j+1])
	ViterbiTable = [[0 for x in range(len(text)+1)] for y in range(len(tags))]
	backpointer = []
	for i in range (len(tags)):
		ViterbiTable[i][1] = lookProb(tagTable,'q_0',tags[i])
		ViterbiTable[i][0] = tags[i]
	backpointer = [[0 for x in range(len(text)+1)] for y in range(len(tags))]
	for i in range(len(backpointer)):
		backpointer[i][0]="q_0"
	count = 0
	for s in range(6):
		index = 0
		for t in range(len(tags)):
			highest = 0.0
			index = 0
			current = []
			for i in range(len(tags)):
				count+=1
				#print tags[t]
				#print lookProb(tagTable,ViterbiTable[t][0],ViterbiTable[i][0])
				#print lookProb(wordTable, ViterbiTable[i][0],text[s+1])
				current.append(float(ViterbiTable[i][s+1])*lookProb(tagTable,ViterbiTable[i][0],ViterbiTable[t][0])*lookProb(wordTable, ViterbiTable[t][0],text[s+1]))
				#print highest
			ViterbiTable[t][s+2] = max(current)
			print current
			print max(current)
			print(np.matrix(ViterbiTable))
			print "current.index(max(current))"
			print current.index(max(current))
			print ViterbiTable[current.index(max(current))][0]
			backpointer[t][s+1]= backpointer[current.index(max(current))][s]+" "+ViterbiTable[t][0]
			#print(np.matrix(ViterbiTable))
			print(np.matrix(backpointer))
	#print "backpointer"
	#print backpointer
	print(np.matrix(ViterbiTable))
	#ViterbiTable = max(ViterbiTable*lookProb('q_f'))
	#backpointer.append(ViterbiTable[s][t])*lookProb('q_f')
	print backpointer
	return backpointer


if __name__ == '__main__':
	with open('corpus', 'r') as file:
		text = file.readlines()	
	textprocessed = ""
	for element in text:
		textprocessed += ' /q_0 '+element+' /q_f '
	#print textprocessed
	tokenizetext = tokenize_text(textprocessed)
	word = tokenizetext[0]
	tag = tokenizetext[1]
	wordset = set(word)
	tagset = set(tag)
	tagset.discard('q_0')
	tagset.discard('q_f')
	#print tag
	Ttable = tagTable(tag, tagset, len(tagset))
	#tag = filter(lambda a: a != 'q_f', tag)
	#tag = filter(lambda a: a != 'q_0', tag)
	temptagset = set(tag)
	temptagset.discard('q_0')
	temptagset.discard('q_f')
	Wtable = wordTable(word, wordset, len(wordset), tag, temptagset, len(temptagset))
	tagTable = TableProb(Ttable)
	wordTable = TableProb(Wtable)
	lookProb(wordTable, 'NOUN', 'the')
	testtext = "show your light when nothing is shining"
	testtag1 = "NOUN PRON NOUN ADV NOUN VERB NOUN"
	testtag2 = "VERB PRON NOUN ADV NOUN VERB VERB"
	testtag3 = "VERB PRON NOUN ADV NOUN VERB NOUN"
	#print calcProb(testtext.split(), testtag1.split(), tagTable, wordTable)
	#print calcProb(testtext.split(), testtag2.split(), tagTable, wordTable)
	#print calcProb(testtext.split(), testtag3.split(), tagTable, wordTable)
	Viterbi(testtext.split(),tagTable,wordTable)


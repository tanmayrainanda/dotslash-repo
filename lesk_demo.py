import nltk 
from nltk.wsd import lesk 
from nltk.tokenize import word_tokenize 
nltk.download('all')
# referred from https://www.geeksforgeeks.org/lesk-algorithm-in-nlp-python/
def get_semantic(seq, key_word): 
	
	# Tokenization of the sequence 
	temp = word_tokenize(seq) 
	
	# Retrieving the definition 
	# of the tokens 
	temp = lesk(temp, key_word) 
	return temp.definition() 
keyword = 'bank'
seq1 = 'we need to deposit money in the bank located near the river bank'
# seq2 = 'The table was already booked by someone else.'

print(get_semantic(seq1, keyword)) 
# print(get_semantic(seq2, keyword)) 

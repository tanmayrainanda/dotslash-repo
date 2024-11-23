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

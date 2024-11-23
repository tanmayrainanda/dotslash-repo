import nltk
tokenizer = nltk.tokenize.RegexpTokenizer('[^\w\']+', gaps=True)
text = 'My name is Aarav and I am a student of class 10th. I am learning Python.'
tokens = tokenizer.tokenize(text)
tokens = [w for w in tokens if not w in nltk.corpus.stopwords.words('english')]
print(tokens)
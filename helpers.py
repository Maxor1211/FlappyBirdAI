# Preprocessing stage
import nltk
import pickle
from word_forms import lemmatizer
from nltk.stem import WordNetLemmatizer
import os
from pathlib import Path

# Create a cache directoy where we do our processing/training
# This won't get committed to the git repository
try:
	os.mkdir(Path("./.cache"))
except FileExistsError:
	pass

try:
	os.mkdir(Path("./.cache/crc"))
except FileExistsError:
	pass

try:
	os.mkdir(Path("./.cache/graphics"))
except FileExistsError:
	pass

os.environ["NLTK_DATA"] = str(Path("./.cache/nltk_data"))
nltk.download("wordnet", Path("./.cache/nltk_data"))
nltk.download("omw-1.4", Path("./.cache/nltk_data"))

# Below code converts dataset to usable form, taken from various NLP tutorials
class Tokenizer:
	def __init__(self):
		self._tokenizer = nltk.RegexpTokenizer(r"\w+")

	def tokenize(self, document: str) -> list:
		return self._tokenizer.tokenize(document)


# Stemmer using the word_forms package
# not usually done this way, other projects use
# the Porter Stemming algorithm
class Stemmer:
	def __init__(self):
		# This word_forms lemmatizer is a bit of a misnomer
		# it does a form of stemming, not lemmatizing
		self._stemmer = lemmatizer
		self._tokenizer = Tokenizer()

	def stem_word(self, word):
		if word == "":
			return ""
		try:
			return self._stemmer.lemmatize(word)
		except ValueError:
			return word

	def stem_sentence(self, sentence):
		result = []
		for word in self._tokenizer.tokenize(sentence):
			result.append(self.stem_word(word))
		return " ".join(result)

	def stem_document(self, document):
		result = []
		for line in document.split("\n"):
			result.append(self.stem_sentence(line))
		return "\n".join(result)


# NLTK-specific lemmatizer from another project
class Lemmatizer:
	def __init__(self):
		self._lemmatizer = WordNetLemmatizer()
		self._tokenizer = Tokenizer()

	def _tokenize(self, document: str) -> list:
		return self._tokenizer.tokenize(document)

	def lemmatize_word(self, word: str, pos=None) -> str:
		return (
			self._lemmatizer.lemmatize(word, pos)
			if pos is not None
			else self._lemmatizer.lemmatize(word)
		)

	def lemmatize_sentence(self, sentence: str, pos=None) -> str:
		result = []
		for word in self._tokenize(sentence):
			if pos is not None:
				result.append(self.lemmatize_word(word, pos))
			else:
				result.append(self.lemmatize_word(word))
		return " ".join(result)

	def lemmatize_document(self, document: str) -> str:
		result = []
		for line in document.split("\n"):
			result.append(self.lemmatize_sentence(line))
		return "\n".join(result)


# These are original contributions
from hashlib import sha1


def pickle_to_file(filename, obj):
	with open(Path(f"./.cache/{filename}.pkl"), "wb") as file:
		pickle.dump(obj, file)


def get_file_hash(file):
	h = sha1()
	with open(file, "rb") as f:
		while True:
			chunk = f.read(h.block_size)
			if not chunk:
				break
			h.update(chunk)
	return h.hexdigest()


def file_has_changed(file):
	try:
		with open("./.cache/crc/" + Path(file).name, "r") as f:
			old_hash = f.readline()
		return get_file_hash(file) == old_hash.strip()
	except FileNotFoundError:
		with open("./.cache/crc/" + Path(file).name, "w") as f:
			f.writelines([get_file_hash(file)])
		return True

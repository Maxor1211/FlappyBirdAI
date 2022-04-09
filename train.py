from attr import has
import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
import math, pickle, time

import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split

from helpers import pickle_to_file, file_has_changed
from helpers import Lemmatizer
from helpers import Stemmer


class text_data:
	def __init__(self, file=None, label=None) -> None:
		self._count_vect = CountVectorizer()
		self._tf_transformer = TfidfTransformer()
		self._lemmatizer = Lemmatizer()
		self._stemmer = Stemmer()
		if file is not None and label is not None:
			# Read the CSV passed into the constructor
			self._data = pd.read_csv(Path(file))
			# For each record create a Python list with the label provided
			# as an argument to the constructor for this object
			self._label = [label for i in range(self._data.shape[0])]
			self._files = [file]

	def __add__(self, other):
		new_text_data = text_data()
		new_text_data._label = self._label + other._label
		new_text_data._data = pd.concat([self._data, other._data])
		new_text_data._files = self._files + other._files
		return new_text_data

	# Text should be array with first two items as follows:
	# ['title', 'text']
	def process_text(self, text):
		if hasattr(self, "_processed_rows"):
			print(
				f"Processed record {self._processed_rows} out of {self._total_rows} ({math.floor(self._processed_rows/self._total_rows*100)}%, {math.floor((time.time() - self._start_time)/(self._processed_rows+1) * (self._total_rows-self._processed_rows))} seconds left)",
				end="\r",
			)
			self._processed_rows += 1
		stemmed = self._stemmer.stem_sentence(text)
		return self._lemmatizer.lemmatize_sentence(stemmed)

	def process_to_x(self):
		filename = "_".join([Path(pathname).name for pathname in self._files])
		print(f"Checking for {filename}...")
		if not Path(f"./.cache/{filename}.pkl").is_file() or not any(
			[file_has_changed(file) for file in self._files]
		):
			print(
				"""Reprocessing the data, this may take a while
It will appear fast up until 50%, as it is going through the titles
Once it reaches the actual text content it will slow down
"""
			)
			self._processed_rows = 0
			self._total_rows = self._data.shape[0] * 2
			self._start_time = time.time()
			# First two columns should be title and text-content
			self._nlp_x = self._data.iloc[:, 0:2].applymap(self.process_text)
			self._nlp_x = pd.concat([self._nlp_x, self._data.iloc[:, 2:4]], axis=1)
			pickle_to_file(filename, self._nlp_x)
			[file_has_changed(file) for file in self._files]
			print("Repickled file as source has changed or cache didn't exist")
			self._processed_rows = -1
			self._total_rows = -1
			self._start_time = -1
		else:
			with open(Path(f"./.cache/{filename}.pkl"), "rb") as file:
				self._nlp_x = pickle.load(file)
			print(
				"Unpickled old file. If this wasn't your intention, delete the crc files in .cache/crc"
			)

	def preprocess(self, nlp_x):
		self._trans_1 = make_column_transformer(
			(self._count_vect, 0), (self._count_vect, 1)
		)
		self.x_preprocessed_count = self._trans_1.fit_transform(
			self._nlp_x.iloc[:, 0:2]
		)
		print("Count", self.x_preprocessed_count.shape)
		self._trans_2 = make_column_transformer(
			(
				self._tf_transformer,
				[i for i in range(0, self.x_preprocessed_count.shape[1])],
			)
		)
		self.x_preprocessed_tfidf = self._trans_2.fit_transform(
			self.x_preprocessed_count
		)
		print("tfidf", self.x_preprocessed_tfidf.shape)

	# Classifiers are numbered based on their ID in the website
	# 0 = dtree, 1 = naive_bayes, 2 = KNN, 3 = SVM
	# if 0 then the tuple decodes to (dtree, criterion, max_depth, min_samples_leaf, min_samples_split)
	# if 1 then the tuple decodes to (nb,)
	# if 2 then the tuple decodes to (knn, k_neighbours, weights, p_minkowski)
	# if 3 then the tuple decodes to (svm)
	def train(
		self, classifier=(0, "entropy", 4, 1000, 1000), train_anew=False, percent_for_test=0
	):

	# TODO: TAKE ADVANTAGE OF THE CONSISTENT API IN SKLEARN


		if percent_for_test != 0:
			(X_train, X_test, y_train, y_test) = train_test_split(
				self.x_preprocessed_tfidf, self._label, test_size=percent_for_test
			)
		else:
			X_train = self.x_preprocessed_tfidf
			y_train = self._label
			X_test = y_test = None
		if classifier[0] == 0:
			# Decision tree
			criterion = classifier[1]
			max_depth = classifier[2]
			min_samples_leaf = classifier[3]
			min_samples_split = classifier[4]
			pkl_stored_at = f"dtree_{criterion}_{max_depth}_{min_samples_leaf}"
			if train_anew or not Path(f"./.cache/{pkl_stored_at}.pkl").is_file():
				self.dtree = DecisionTreeClassifier(
					criterion=criterion,
					max_depth=max_depth,
					min_samples_split=min_samples_split,
					min_samples_leaf=min_samples_leaf,
				)
				self.dtree.fit(X_train, y_train)
				pickle_to_file(f"{pkl_stored_at}", self.dtree)
			else:
				with open(Path(f"./.cache/{pkl_stored_at}.pkl"), "rb") as file:
					self.dtree = pickle.load(file)
			sklearn.tree.plot_tree(self.dtree)
			plt.savefig(Path(f"./.cache/graphics/{pkl_stored_at}.svg"))
			return [
				self.dtree.score(X_train, y_train),
				self.dtree.score(X_test, y_test)
				if (X_test is not None and y_test is not None)
				else 0,
				[f"./.cache/graphics/{pkl_stored_at}.svg"],
			]
		elif classifier[0] == 1:
			# Naive Bayes
			pass
		elif classifier[0] == 2:
			# k-Nearest-Neighbours
			n_neighbors = classifier[1]
			weights = classifier[2]
			power = classifier[3]
			pkl_stored_at = f"knn_{n_neighbors}_{weights}_{power}"
			if train_anew or not Path(f"./.cache/{pkl_stored_at}.pkl").is_file():
				self.knn = KNeighborsClassifier(
					n_neighbors=n_neighbors, weights=weights, p=power, n_jobs=-1
				)
				self.knn.fit(X_train, y_train)
				pickle_to_file(f"{pkl_stored_at}", self.knn)
			else:
				with open(Path(f"./.cache/{pkl_stored_at}.pkl"), "rb") as file:
					self.knn = pickle.load(file)
			return [
				0,#self.knn.score(X_train, y_train),
				self.knn.score(X_test, y_test)
				if (X_test is not None and y_test is not None)
				else 0,
				[],
			]
		elif classifier[0] == 3:
			# SVM
			pass

	def predict(self, title, text, classifiers=[0]):
		df = pd.DataFrame(data={"title": [title], "text": [text]})
		nlp_df = df.applymap(self.process_text)
		out_1 = self._trans_1.transform(nlp_df)
		out_2 = self._trans_2.transform(out_1)
		result = []
		if 0 in classifiers:
			result.append(self.dtree.predict(out_2))
		if 1 in classifiers:
			result.append(self.nb.predict(out_2))
		if 2 in classifiers:
			result.append(self.knn.predict(out_2))
		if 3 in classifiers:
			result.append(self.svm.predict(out_2))
		return result


def create_classifiers():
	# Read the data from files, with label 0 for fake and 1 for true
	fake_data = text_data(Path("./datasets/1/Fake.csv"), 0)
	true_data = text_data(Path("./datasets/1/True.csv"), 1)
	# I overloaded the + operator to append the labels, and to concatenate the Pandas DataFrames
	combined_data = fake_data + true_data
	# Invoke the processing pipeline to do NLP for us
	combined_data.process_to_x()
	# print(combined_data._nlp_x)
	# print(combined_data._nlp_x.shape)
	# with pd.option_context("display.max_columns", 20):
	# 	print(combined_data._nlp_x.head(10))
	combined_data.preprocess(combined_data._nlp_x)
	print("DTREE",combined_data.train(
		classifier=(0, "entropy", 4, 200), train_anew=False, percent_for_test=0
	))
	print("KNN",combined_data.train(
		classifier=(2, 20, "uniform", 2), train_anew=False, percent_for_test=0
	))
	return combined_data


if __name__ == "__main__":
	create_classifiers()

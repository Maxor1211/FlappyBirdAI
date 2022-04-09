import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from pathlib import Path

from train import text_data

import pandas as pd
import math, pickle, time

fake_data = text_data(Path("./datasets/1/Fake.csv"), 0)
true_data = text_data(Path("./datasets/1/True.csv"), 1)
# I overloaded the + operator to append the labels, and to concatenate the Pandas DataFrames
combined_data = fake_data + true_data
combined_data.process_to_x()
combined_data.preprocess(combined_data._nlp_x)

test_scores=[]
train_scores=[]
node_count=[]

print("Holdout method, decision tree, default hyperparametes")
for i in range(10):
	(X_train, X_test, y_train, y_test) = train_test_split(combined_data.x_preprocessed_tfidf, combined_data._label, test_size=0.2)
	# Decision tree
	dtree = DecisionTreeClassifier(
		criterion="entropy"
	)
	dtree.fit(X_train, y_train)
	sklearn.tree.plot_tree(dtree)
	plt.savefig(Path(f"./.cache/graphics/report/output_default_dtree_{i}.svg"))

	test_score = dtree.score(X_test, y_test)
	train_score = dtree.score(X_train, y_train)
	test_scores.append(test_score)
	train_scores.append(train_score)
	node_count.append(dtree.tree_.node_count)
	print(
		f"Iteration {i}",
		f"Train score {train_score}",
		f"Test score {test_score}"
		if (X_test is not None and y_test is not None)
		else 0,
		f"Node count is {dtree.tree_.node_count}",
		f"Number of leaves {dtree.get_n_leaves()}"
	)

print(f"Test avg: {sum(test_scores)/10}")
print(f"train avg: {sum(train_scores)/10}")

test_scores_2=[]
train_scores_2=[]
for j in range(4):
	print("Holdout method, decision tree, tweaked hyperparametes")
	print(f"Max depth {4+j*2},  min samples split {1000+j*2000},  min samples leaf {750+j*1500}")
	test_scores_per_run=[]
	train_scores_per_run=[]
	for i in range(10):
		(X_train, X_test, y_train, y_test) = train_test_split(combined_data.x_preprocessed_tfidf, combined_data._label, test_size=0.2)
		# Decision tree
		dtree = DecisionTreeClassifier(
			criterion="entropy",
			max_depth=4+j*2,
			min_samples_split=1000+j*2000,
			min_samples_leaf=750+j*1500
		)
		dtree.fit(X_train, y_train)
		sklearn.tree.plot_tree(dtree)
		plt.savefig(Path(f"./.cache/graphics/report/output_dtree_{i}_mdepth-{4+j*2}_mssplit-{1000+j*2000}_msleaf-{750+j*1500}.svg"))

		test_score = dtree.score(X_test, y_test)
		train_score = dtree.score(X_train, y_train)
		test_scores_2.append(test_score)
		train_scores_2.append(train_score)
		test_scores_per_run.append(test_score)
		train_scores_per_run.append(train_score)
		node_count.append(dtree.tree_.node_count)
		print(
			f"Iteration {i}",
			f"Train score {train_score}",
			f"Test score {test_score}"
			if (X_test is not None and y_test is not None)
			else 0,
			f"Node count is {dtree.tree_.node_count}",
			f"Number of leaves {dtree.get_n_leaves()}"
		)

	print(f"Test avg: {sum(test_scores_per_run)/10}")
	print(f"train avg: {sum(train_scores_per_run)/10}")

print(f"Test avg of all tweaked runs: {sum(test_scores_2)/10}")
print(f"train avg of all tweaked runs: {sum(train_scores_2)/10}")

plt.figure()

plt.plot(node_count,(test_scores+test_scores_2),label="Default dtree")
plt.plot(node_count,(train_scores+train_scores_2),label="Tweaked dtree")
plt.savefig(Path(f"./.cache/graphics/report/complexity_graph.svg"))
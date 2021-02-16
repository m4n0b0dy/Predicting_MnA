import tensorflow as tf
import numpy as np
import pandas as pd
#not going to inherit from glas class and Node2Vec class
#was getting annoyingly complex and seemed like bad practice
class GraphML:

	'''
	TODO
	Implement Base Graph ML object to train, test, and evaluate models
	inhereit from a base graph class
	also performance metrics
	'''
	def __init__(self):
		pass
		
	#todo
	def train_test_split(self):
		pass
	#todo
	def train(self):
		pass
	#todo
	def test(self):
		pass
	
	#todo
	def evaluate(self):
		pass

	def transform(self):
		pass

	@property
	def embeddings(self):
		return self._embedding

	@property
	def embeddings_as_df(self):
		return pd.DataFrame(self.embeddings).transpose()
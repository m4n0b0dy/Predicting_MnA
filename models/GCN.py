import tensorflow as tf
import sys
sys.path.insert(0, '../')
from models.GraphML import GraphML
class GraphGCN(GraphML):
	def __init__(self, *args, **kwargs):
		GraphML.__init__(self, *args, **kwargs)
	'''
	TODO
	Implement Graph Convolutional network, inheriting from a base graph ML object
	'''
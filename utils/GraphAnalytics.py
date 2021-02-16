import sys
sys.path.insert(0, '../')
from utils.BaseGraph import BaseGraph
import networkx as nx
class GraphAnalytics(BaseGraph):
	'''
	Implement Graph analytics object for all relevant analyttics
	since we are using inheritance, can steal 
	'''

	@property
	@BaseGraph.run_as_digraph
	def clustering_coef(self):
		return nx.algorithms.cluster.clustering(self)

	@property
	@BaseGraph.run_as_digraph
	def transitivity(self):
		return nx.algorithms.cluster.transitivity(self)

	@property
	@BaseGraph.run_as_graph
	#@BaseGraph.run_as_undigraph
	#had to get rid of this decorator. Couldn't find the best way to overwrite the entire instance of graph
	#object on a conversion. As a result, converting it creates and returns a new graph (see BaseGraph @property methods)
	#Because we are creating a new graph, there is no longer a decorator to call
	def triangles(self):
		return nx.algorithms.cluster.triangles(self.to_undirected())
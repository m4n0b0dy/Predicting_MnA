import sys
sys.path.insert(0, '../')
from models.GraphML import GraphML
from karateclub import Node2Vec
from gensim.models.word2vec import Word2Vec
from karateclub.utils.walker import BiasedRandomWalker
import networkx as nx
class GraphNode2Vec(GraphML, Node2Vec):
	def __init__(self, *args, **kwargs):
		Node2Vec.__init__(self, *args, **kwargs)
		GraphML.__init__(self, *args, **kwargs)

	def fit(self, graph):
		"""
		Fitting a DeepWalk model.
		Arg types:
			* **graph** *(NetworkX graph)* - The graph to be embedded.
		"""
		self._set_seed()
		walker = BiasedRandomWalker(self.walk_length,
			self.walk_number,
			self.p, self.q)
		walker.do_walks(graph)

		model = Word2Vec(walker.walks,
						 hs=1,
						 alpha=self.learning_rate,
						 iter=self.epochs,
						 size=self.dimensions,
						 window=self.window_size,
						 min_count=self.min_count,
						 workers=self.workers,
						 seed=self.seed)

		self._embedding = {n:model[str(n)] for n in graph.nodes}
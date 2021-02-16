
from neo4j import GraphDatabase
import networkx as nx
import pickle
import pandas as pd
import numpy as np

class BaseGraph(nx.MultiDiGraph):
	'''
	Implement Base Graph object read data,
	inhereit from whatever networkx object is best, etc
	repurpose functions here as methods
	'''
	def __init__(self, *args, **kwargs):
		super(BaseGraph, self).__init__(*args, **kwargs)
		self.driver = None

	def connect_to_neo(self, conn_dic:dict,
		encrypted_bool:bool = False) -> None:

		from neo4j import GraphDatabase
		uri = conn_dic['url']
		port = conn_dic['port']
		user = conn_dic['user']
		password = conn_dic['password']
		self.driver = GraphDatabase.driver(uri+':'+port,
			auth=(user, password), encrypted=encrypted_bool)
		#test
		self.pull_from_neo("Match () Return 1 Limit 1")
		print('Connection Succesful')

	@property #makes sense!
	def adjacency_matrix(self):
		return nx.convert_matrix.to_numpy_array(self)

	def overwrite_graph(self, new_graph):
		self.clear()
		self.add_nodes_from(new_graph)
		self.add_edges_from(new_graph.edges)

	#https://stackoverflow.com/questions/59289134/constructing-networkx-graph-from-neo4j-query-result
	def pull_from_neo(self, query:str, overwrite:bool = False):

		results = self.driver.session().run(query)
		_tmp_graph = BaseGraph()

		for node in list(results.graph()._nodes.values()):
			try:
				labels = [_ for _ in node._labels if _!= 'Tmp'][0]
			except:
				continue
			_tmp_graph.add_node(node.id,
				labels=labels,
				properties=node._properties)

		rels = list(results.graph()._relationships.values())
		for rel in rels:
			_tmp_graph.add_edge(rel.start_node.id,
				rel.end_node.id,
				key=rel.id,
				type=rel.type,
				properties=rel._properties)
		if overwrite:
			#clears graph and copies in from tmp
			self.overwrite_graph(_tmp_graph)
		else:
			return _tmp_graph

	def pull_full_graph(self, overwrite = True, limit = '500'):
		query = """MATCH (n)-[r]->(c) RETURN *"""
		if limit:
			query += ' LIMIT '+limit
		self.pull_from_neo(query = query,
			overwrite = overwrite)

	def load_graph(self, fname):
		self.overwrite_graph(nx.read_gpickle(fname+".gpickle"))

	def save_graph(self, fname):
		#Can't pickle neo4j driver!
		self.driver = None
		nx.write_gpickle(self, fname+".gpickle")

	#conversion attributes and decorators
	@property
	def as_digraph(self):
		return nx.DiGraph(self)

	@property
	def as_undigraph(self):
		return self.to_undirected(self)

	@property
	def as_graph(self):
		return nx.Graph(self)

	#tried to give these their own decorator to prevent copy/paste couldn't get a good example
	@staticmethod
	def run_as_digraph(func):
		def _run_func(_graph):
			return func(_graph.as_digraph)
		return _run_func

	@staticmethod
	def run_as_undigraph(func):
		def _run_func(_graph):
			return func(_graph.as_undigraph)
		return _run_func

	@staticmethod
	def run_as_graph(func):
		def _run_func(_graph):
			return func(_graph.as_graph)
		return _run_func
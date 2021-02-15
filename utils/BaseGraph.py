#https://stackoverflow.com/questions/59289134/constructing-networkx-graph-from-neo4j-query-result
from neo4j import GraphDatabase
import networkx as nx
import pickle
import pandas as pd
import numpy as np

class BaseGraph(nx):
	'''
	TODO
	Implement Base Graph object read data, inhereit from whatever networkx object is best, etc
	repurpose functions here as methods
	'''
	#todo
	def __init__(self):
		pass
	#rewrite these as methods
	#todo
	def connect_to_neo(self):
		pass

	#todo
	def get_adjacency_matrix(self):
		pass

	def pull_from_neo(driver, query):

		results = driver.session().run(query)
		G = nx.MultiDiGraph()
		#G = nx.DiGraph() #TODO
		nodes = list(results.graph()._nodes.values())
		for node in nodes:
			try:
				labels = [_ for _ in node._labels if _!= 'Tmp'][0]
			except:
				continue
			G.add_node(node.id,
				labels=labels,
				properties=node._properties)

		rels = list(results.graph()._relationships.values())
		for rel in rels:
			G.add_edge(rel.start_node.id,
				rel.end_node.id,
				key=rel.id,
				type=rel.type,
				properties=rel._properties)
		return G

	def load_graph(self, fname):
		G = nx.read_gpickle(fname+".gpickle")
		return G
	def save_graph(self, fname):
		nx.write_gpickle(self.G, fname+".gpickle")

	
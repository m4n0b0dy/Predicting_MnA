#https://stackoverflow.com/questions/59289134/constructing-networkx-graph-from-neo4j-query-result
from neo4j import GraphDatabase
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import pandas as pd



def new_graph_from_cypher(driver, query):

	results = driver.session().run(query)
	G = nx.MultiDiGraph()
	#G = nx.DiGraph()
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

def graph_viz(G, title='',
				  labels='labels',
				  cat_colors={},
				  node_options={"node_size":50, "alpha":1.0},
				  edge_options={"width":1.0,"edge_color":"black", "alpha":1},
				  unk_node_options={"node_size":50, "alpha":.5, "node_color":"red"},
				  pos_func=nx.spring_layout, size=(10,10)):
	G.fig, _ = plt.subplots(figsize=size)
	pos = pos_func(G)
	_.set_title(title)
	
	if labels and cat_colors:
		label_values = set(nx.get_node_attributes(G, labels).values())
		for label_value in label_values:
			nx.draw_networkx_nodes(G, pos,
								   nodelist=[x for x,y in G.nodes().data() if y and y[labels]==label_value],
								   node_color=cat_colors[label_value], **node_options)
		nx.draw_networkx_nodes(G, pos, nodelist=[x for x,y in G.nodes().data() if not y], **unk_node_options)
	else:
		nx.draw_networkx_nodes(G, pos, **node_options)
	nx.draw_networkx_edges(G, pos, **edge_options)
	plt.show()

def load_data(fname):

	G = nx.read_gpickle(fname+".gpickle")
	return G
def save_data(G, fname):
	nx.write_gpickle(G, fname+".gpickle")
	
def display_plotly_graphs():#had some errors when trying to view plotly, this function allows you to view plots in jupyter
	import IPython
	display(IPython.core.display.HTML('''
		<script src="/static/components/requirejs/require.js"></script>
		<script>
		  requirejs.config({
			paths: {
			  base: '/static/base',
			  plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
			},
		  });
		</script>
		'''))

def histogram(G, title='', bins=50, color='blue', metric=''):
	px.histogram(G.sort_values(metric), x=metric, title=title, nbins=bins, color_discrete_sequence=[color]).show()
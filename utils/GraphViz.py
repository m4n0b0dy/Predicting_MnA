import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
from BaseGraph import BaseGraph

class GraphViz(BaseGraph):
	'''
	TODO
	Implement Graph viz object for all visualizations
	'''
	#change all G to self.G

	def network_viz(G, title='',
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
		

	def histogram(G, title='', bins=50, color='blue', metric=''):
		px.histogram(G.sort_values(metric), x=metric, title=title, nbins=bins, color_discrete_sequence=[color]).show()

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
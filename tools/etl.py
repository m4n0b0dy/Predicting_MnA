import pandas as pd
import numpy as np
from multiprocessing.pool import ThreadPool as Pool
from os import path
from os import listdir
import sys
sys.path.insert(0, '../configs/')
from etl_config import *
from sparql_config import ENTITY_PATH, EDGE_PATH, COUNTRIES

THREAD_COUNT = 100

def clean_wiki(df):
	for c in df.columns:
		try:
			df[c] = df[c].str.replace('http://www.wikidata.org/entity/','')
		except:
			pass
	return df

def etl_entities(raw_df):
	raw_df = clean_wiki(raw_df)
	df = pd.DataFrame(columns=list(ENTITY_COLUMNS))
	prev_cols = [_ for _ in list(ENTITY_COLUMNS) if _ in raw_df.columns]
	df[prev_cols] = raw_df[prev_cols]
	df.columns = df.columns.map(ENTITY_COLUMNS)
	val_cols = [_ for _ in df.columns if '_vals' in _]
	quant_cols = [_ for _ in df.columns if '_quant' in _]
	for col in quant_cols:
		df[col] = df[col].astype(str).str.extract('(\d+)', expand=False)
		df[col] = df[col].astype(float).fillna(0)
		labels = [str(_)+'_'+col.replace('_quant','') for _ in range(0,10)]
		df[col] = pd.cut(df[col], 10, labels=labels)
	val_cols += quant_cols
	ent_df = df.drop(val_cols,axis=1)
	ent_df = ent_df.drop_duplicates().fillna('')
	return df, val_cols

def dic_to_ls(dic,typ,node_typ):
	ret_ls = []
	for k, vs in dic.items():
		for v in vs:
			ret_ls.append({'company_id':k,'val_id':v,'edge_typ':typ,'node_typ':node_typ})
	return ret_ls

def etl_edge_entities(df, val_cols):
	mult_df = df[val_cols+['id']]
	redex = mult_df.copy()
	redex = redex.replace(np.nan, '')
	redex.index = mult_df['id']
	ls = dic_to_ls(redex['industry_vals'].dropna().str.split(',').to_dict(), 'INDUSTRY', 'Industry') \
	+ dic_to_ls(redex['ceo_vals'].dropna().str.split(',').to_dict(), 'CEO', 'Person')\
	+ dic_to_ls(redex['chair_vals'].dropna().str.split(',').to_dict(), 'CHAIRMAN', 'Person')\
	+ dic_to_ls(redex['hq_vals'].dropna().str.split(',').to_dict(), 'HEADQUARTERS', 'Location')\
	+ dic_to_ls(redex['group_vals'].dropna().str.split(',').to_dict(),'GROUPED_IN', 'Group')\
	+ dic_to_ls(redex['country_vals'].dropna().str.split(',').to_dict(),'RESIDES_IN', 'Location')\
	+ dic_to_ls(redex['employee_count_quant'].dropna().str.split(',').to_dict(), 'EMPLOYEE_COUNT_BAND', 'Quant_Metric')\
	+ dic_to_ls(redex['profit_quant'].dropna().str.split(',').to_dict(), 'PROFIT_BAND', 'Quant_Metric')\
	+ dic_to_ls(redex['assets_quant'].dropna().str.split(',').to_dict(), 'ASSETS_BAND', 'Quant_Metric')\
	+ dic_to_ls(redex['equity_quant'].dropna().str.split(',').to_dict(), 'EQUITY_BAND', 'Quant_Metric')\
	+ dic_to_ls(redex['market_cap_quant'].dropna().str.split(',').to_dict(),'MARKET_CAP_BAND', 'Quant_Metric')
	ent_edge_df = pd.DataFrame(ls, columns = ['company_id','val_id','edge_typ', 'node_typ'])
	#final etl step specific to my tasks
	ent_edge_df = ent_edge_df[~ent_edge_df['val_id'].str.contains('0_')]
	ent_edge_df = ent_edge_df[ent_edge_df['val_id']!='']
	return ent_edge_df

def etl_edges(raw_df):
	raw_df = clean_wiki(raw_df)
	df = pd.DataFrame(columns=list(EDGE_COLUMNS))
	prev_cols = [_ for _ in list(EDGE_COLUMNS) if _ in raw_df.columns]
	df[prev_cols] = raw_df[prev_cols]
	df.columns = df.columns.map(EDGE_COLUMNS)
	edge_df = df.copy()
	edge_df = edge_df.fillna('')
	return edge_df

def run_etl(country):
	raw_df = pd.read_csv(ENTITY_PATH.format(COUNTRY=country))
	df, val_cols = etl_entities(raw_df)
	ent_df = df.drop(val_cols,axis=1)
	ent_df.drop_duplicates().to_csv(ETL_ENTITY_PATH.format(COUNTRY=country),index=False)
	print(country,'entities etl completed')
	ent_edge_df = etl_edge_entities(df, val_cols)
	if len(ent_edge_df):
		ent_edge_df.drop_duplicates().to_csv(ETL_ENTITY_EDGE_PATH.format(COUNTRY=country),index=False)
	print(country,'entity edges etl completed')
	#now run edge etl
	raw_df = pd.read_csv(EDGE_PATH.format(COUNTRY=country))
	edge_df = etl_edges(raw_df)
	if len(edge_df):
		edge_df.drop_duplicates().to_csv(ETL_EDGE_PATH.format(COUNTRY=country),index=False)
	print(country,'edges etl completed')
#multithreaded extraction
if __name__ == '__main__':
	print('Starting ETL')
	pool = Pool(THREAD_COUNT)
	pool.map(run_etl, COUNTRIES)
	pool.close()
	pool.join()
	print('Completed ETL Extraction')
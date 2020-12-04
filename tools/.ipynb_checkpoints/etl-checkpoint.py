import pandas as pd
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
	df = df.fillna('')
	return df, val_cols

def dic_to_ls(dic,typ):
	ret_ls = []
	for k, vs in dic.items():
		for v in vs:
			ret_ls.append({'company_id':k,'val_id':v,'typ':typ})
	return ret_ls

def etl_edge_entities(df, val_cols):
	mult_df = df[val_cols+['id']]
	redex = mult_df.copy()
	redex.index = mult_df['id']
	ind_ls = dic_to_ls(redex['industry_vals'].dropna().str.split(',').to_dict(), 'INDUSTRY')
	ceo_ls = dic_to_ls(redex['ceo_vals'].dropna().str.split(',').to_dict(), 'CEO')
	chair_ls = dic_to_ls(redex['chair_vals'].dropna().str.split(',').to_dict(), 'CHAIRMAN')
	hq_ls = dic_to_ls(redex['hq_vals'].dropna().str.split(',').to_dict(), 'HEADQUARTERS')
	group_ls = dic_to_ls(redex['group_vals'].dropna().str.split(',').to_dict(),'GROUPED_IN')
	country_ls = dic_to_ls(redex['country_vals'].dropna().str.split(',').to_dict(),'RESIDES_IN')
	ent_edge_df = pd.DataFrame(ind_ls+ceo_ls+chair_ls+hq_ls+group_ls+country_ls, columns = ['company_id','val_id','typ'])
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
	ent_edge_df.drop_duplicates().to_csv(ETL_ENTITY_EDGE_PATH.format(COUNTRY=country),index=False)
	print(country,'entity edges etl completed')
	#now run edge etl
	raw_df = pd.read_csv(EDGE_PATH.format(COUNTRY=country))
	edge_df = etl_edges(raw_df)
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
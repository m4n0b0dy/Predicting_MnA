ENTITY_COLUMNS = {'business.value':'id',
'businessLabel.value':'name',
'origindate.value':'start_date',
'country.value':'country_vals',
'industries.value':'industry_vals',
'ceos.value':'ceo_vals',
'chairs.value':'chair_vals',
'hqs.value':'hq_vals',
'groups.value':'group_vals',
'employees.value':'employee_count_quant',
'profit.value':'profit_quant',
'assets.value':'assets_quant', 
'equity.value':'equity_quant',
'markcap.value':'market_cap_quant'}

ETL_ENTITY_PATH = '../data/ingestion/entities/{COUNTRY}.csv'
ETL_ENTITY_EDGE_PATH = '../data/ingestion/prop_edges/{COUNTRY}.csv'

EDGE_COLUMNS = {'company.value':'owned_id',
'owner.value':'owner_id',
'acquiredate.value':'date'}

ETL_EDGE_PATH = '../data/ingestion/acq_edges/{COUNTRY}.csv'
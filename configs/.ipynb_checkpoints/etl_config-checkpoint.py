ENTITY_COLUMNS = {'business.value':'id',
'businessLabel.value':'name',
'origindate.value':'start_date',
'country.value':'country',
'industries.value':'industry_vals',
'ceos.value':'ceo_vals',
'chairs.value':'chair_vals',
'hqs.value':'hq_vals',
'groups.value':'group_vals',
'employees.value':'employee_count',
'profit.value':'profit',
'assets.value':'assets',
'equity.value':'equity',
'markcap.value':'market_cap'}

ETL_ENTITY_PATH = '../data/ingestion/entities/{COUNTRY}.csv'
ETL_ENTITY_EDGE_PATH = '../data/ingestion/edges/no_date/{COUNTRY}.csv'

EDGE_COLUMNS = {'company.value':'owned_id',
'companyLabel.value':'owned_name',
'owner.value':'owner_id',
'ownerLabel.value':'owner_name',
'acquiredate.value':'date'}

ETL_EDGE_PATH = '../data/ingestion/edges/with_date/{COUNTRY}.csv'
#Config to use when running locally / with mysql
config_db = {
    'user': 'root',
    'password': 'password',
    'host': "localhost",
    'database': 'DBPIPELINE_DB',
    'raise_on_warnings': True,
    'port': '8321'
}

#Current Postgres config setup
config_warehouse = {
    'user': 'root',
    'password': 'password',
    'host': "localhost",
    'database': 'DBPIPELINE_WAREHOUSE',
    'raise_on_warnings': True,
    'port': 5444
}
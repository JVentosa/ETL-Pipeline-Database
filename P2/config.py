# Config to use when running locally / with mysql
config_db = {
    'user': 'root',
    'password': 'password',
    'host': "localhost",
    'database': 'DBPIPELINE_DB',
    'raise_on_warnings': True,
    'port': 3306
}

# Current Postgres config setup
config_warehouse = {
    'user': 'root',
    'password': 'password',
    'host': "localhost",
    'database': 'Pipe',
    'raise_on_warnings': True,
    'port': 5432
}

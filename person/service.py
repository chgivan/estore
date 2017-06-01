import os, sys, psycopg2

def _getEnvVariable(name):
    variable = os.environ.get(name)
    if variable is None:
        print("[ERROR] Missing Environment Variable " + str(name))
        sys.exit(-1)
    return variable

dbUser = _getEnvVariable("POSTGRES_USER")
dbPass = _getEnvVariable('POSTGRES_PASSWORD')
dbName = _getEnvVariable('POSTGRES_DB')
dbHost = _getEnvVariable('POSTGRES_HOST')

try:
    conn = psycopg2.connect(dbname=dbName, user=dbUser, host=dbHost, password=dbPass)
    cur = conn.cursor()
except:
    print("[ERROR] Unable to connect to the database" + dbname + "@" + dbHost)
    sys.exit(-1)

cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")

cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
conn.commit()

cur.close()
conn.close()

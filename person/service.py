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

createPersonTableSQL = """
    CREATE TABLE IF NOT EXISTS persons (
        id serial PRIMARY KEY,
        firstName varchar(50) NOT NULL,
        lastName varchar(50) NOT NULL,
        email varchar(50) UNIQUE NOT NULL,
        role varchar(5) NOT NULL CHECK (role IN ('admin','user'))
    );
"""

insertPersonSQL = """
    INSERT INTO persons (firstName, lastName, email, role)
    VALUES (%(firstName)s, %(lastName)s, %(email)s, %(role)s );
"""

cur.execute(createPersonTableSQL)
conn.commit()

class person:
    id = None
    firstName = None
    lastName = None
    email = None
    role = None

loadLite(id):

loadPerson(id):
    >>> cur.execute("SELECT id, firstName, lastName, email, role FROM test;")
>>> cur.fetchone()
(1, 100, "abc'def")


cur.execute(insertPersonSQL, {
    'firstName': "Test 3",
    'lastName': "Testopoulos 3",
    'email': "Testopoulos 3@test.test",
    'role': "asa"
})
conn.commit()

cur.close()
conn.close()

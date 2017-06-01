import os, sys, psycopg2
import sqlTemplates as sql

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
    cur.execute(sql.createPersonTableSQL)
    conn.commit()
except:
    print("[ERROR] Unable to connect to the database" + dbname + "@" + dbHost)
    sys.exit(-1)



def createPerson(body):
    try:
        cur.execute(sql.insertPersonSQL, body)
        id = cur.fetchone()[0]
        conn.commit()
        return id
    except psycopg2.IntegrityError as err:
        conn.rollback()
        if err.pgcode == '23505': #unique_violation
            pass
        elif err.pgcode == '23514': #check_violation
            pass
        else:
            pass
        print("[DBError](person.create) Code:" + err.pgcode , str(err))
        return None;
    except Exception as err:
        print("[Error](person.create) " + str(err))
        return None;

def getPerson(id):
    try:
        cur.execute(sql.selectFullPersonSQL, {'id':id})
        row = cur.fetchone()
        if row is None:
            print("[ArgsError](person.get) Unknown id " + id)
            return None
        print(row)
        return sql.convertRow2Person(row)
    except psycopg2.IntegrityError as err:
        print("[DBError](person.get) Code:" + err.pgcode , str(err))
        return None;
    except Exception as err:
        print("[Error](person.get) " + str(err))
        return None;

def getAllPersonIDs():
    try:
        cur.execute(sql.selectAllIdsSQL)
        rows = cur.fetchall()
        body = []
        for row in rows:
            body.append(row[0])
        return body
    except psycopg2.IntegrityError as err:
        print("[DBError](person.getAll) Code:" + err.pgcode , str(err))
        return None;
    except Exception as err:
        print("[Error](person.getAll)" + str(err))
        return None;
'''
id = createPerson({
    'firstName': "saffas",
    'lastName': "Testopoulos 4",
    'email': "Testopoulos 1@test.test",
    'role': "admin"
})
print(id)
'''

print(getPerson("4"))
print(str(getAllPersonIDs()))


cur.close()
conn.close()

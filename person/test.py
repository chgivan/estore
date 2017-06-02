from pony.orm import *
import os, sys

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
db = Database()

class Person(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    firstName = Required(str)
    lastName = Required(str)
    role = Required(str)

db.bind('postgres', user=dbUser, password=dbPass, host=dbHost, database=dbName)
db.generate_mapping(create_tables=True)
sql_debug(True)
'''
with db_session:
    p1 = Person(email="test1@test.ts", firstName="test1", lastName="testopoulos", role="admin")
    p2 = Person(email="test2@test.ts", firstName="test2", lastName="testopoulos", role="user")
    p3 = Person(email="test3@test.ts", firstName="test3", lastName="testopoulos", role="user")
    p4 = Person(email="test4@test.ts", firstName="test4", lastName="testopoulos", role="user")
    p5 = Person(email="test5@test.ts", firstName="test5", lastName="testopoulos", role="user")
'''
@db_session
def createPerson(email, firstName, lastName, role):
    Person(email=email,firstName=firstName,lastName=lastName,role=role)

createPerson(email="test6@test.ts", firstName="test6", lastName="testopoulos", role="admin")
with db_session:
    print(str(select(p.email for p in Person if p.role == "user")[:]))

from pony.orm import *
from flask import Flask, request, jsonify
import os, sys, json

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
app = Flask(__name__)

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
#BackEnd


@db_session
def updatePerson(id,**body):
    Person[id].set(**body)

@db_session
def deletePerson(id):
    Person[id].delete()

def except_hook(type, value, tback):
    if type is core.ObjectNotFound:
        print("[Error] Person Not Found")
    elif type is core.TransactionIntegrityError:
        print("[Error] Person Duplicate Email")
    elif type is ValueError:
        print("[Error] " + str(value))
    else:
        sys.__excepthook__(type, value, tback)
sys.excepthook = except_hook

@app.route("/", methods=["GET"])
@db_session
def getPersons():
    limit = request.args.get("limit", default=100, type=int)
    persons = Person.select().order_by(lambda p: p.lastName)[:limit]
    return jsonify([p.to_dict() for p in persons])

@app.route("/<id>", methods=["GET"])
@db_session
def getPerson(id):
    try:
        return jsonify(Person[id].to_dict())
    except core.ObjectNotFound:
        response = jsonify({"msg":"Person ID " + id + " does not exists!"})
        response.status_code = 404
        return response
    except:
        response = jsonify({"msg":"Internal Application Error"})
        response.status_code = 500
        return response

@app.route("/", methods=["POST"])
@db_session
def createPerson():
    if not validPersonArgs():
        response = jsonify({"msg":"Bad Request Argument on create Person!"})
        response.status_code = 400
        return response
    p = Person(request.args)
    commit()
    response = jsonify({"id":p.id})
    response.status_code = 201
    return response

def validPersonArgs():
    if set('email','firstName','lastName','role') != request.args.keys():
        return False

if __name__ == "__main__":
    app.run(debug=True)

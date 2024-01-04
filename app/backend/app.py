from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(user, password), database="neo4j")


# Example of flask+neo4j workflow on backend to ease later development:

# GET EMPLOYEES WORKING IN A DEPARTMENT

# def get_employees_by_dept(tx, id):
#     query = f"match (e:Employee)-[r]->(d:Department) WHERE ID(d) = {id} return e"
#     results = tx.run(query).data()
#     if not results:
#         return None
#     else:
#         return [{"name": result["e"]["name"], "surname": result["e"]["surname"], "age": result["e"]["age"]} for result in results]


# @app.route("/departments/<int:id>/employees", methods=["GET"])
# def get_employees_by_dept_route(id):
#     employees = driver.session().read_transaction(get_employees_by_dept, id)
#     print("Received a GET request on endpoint /departments/<id>/employees")
#     return jsonify({"department employees": employees}), 200

@app.route("/", methods=["GET"])
def get_employees_by_dept_route():
    print("Received a GET request on endpoint /")
    return jsonify({}), 200


if __name__ == "__main__":
    app.run()
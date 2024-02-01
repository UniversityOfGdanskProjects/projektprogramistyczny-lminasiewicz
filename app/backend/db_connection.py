import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
auth = (user, password)
driver = GraphDatabase.driver(uri, auth=auth, database="neo4j")
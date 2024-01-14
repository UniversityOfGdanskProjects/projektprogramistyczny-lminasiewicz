import os
import re
import sys
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_uget = Blueprint("bp_uget", __name__)



# GET ALL USERS

def get_users(tx) -> list[dict]:
    query = "match (u:User) return u"
    results = tx.run(query).data()
    return [{"username": result["u"]["username"], "link": result["u"]["link"], "registered": str(result["u"]["registered"])} for result in results]


@bp_uget.route("/api/users", methods=["GET"])
def get_users_route():
    posts = driver.session().execute_read(get_users)
    print("Received a GET request on endpoint /api/users")
    return {"users": posts}, 200



# GET COUNT OF REGISTERED USERS

def get_count_users(tx) -> int:
    query = "match (u:User) return count(u)"
    results = tx.run(query).data()
    return results[0]["count(u)"]


@bp_uget.route("/api/users/count", methods=["GET"])
def get_count_users_route():
    count = driver.session().execute_read(get_count_users)
    print("Received a GET request on endpoint /api/users/count")
    return {"count": count}, 200


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



# GET USERS BY SEARCHED PHRASE

def get_users_search(tx, search: str) -> list[dict]:
    query = f"match (u:User) where toLower(u.username) contains \"{search}\" return u"
    results = tx.run(query).data()
    return [{"username": result["u"]["username"], "link": result["u"]["link"], "registered": str(result["u"]["registered"])} for result in results]


@bp_uget.route("/api/users/search", methods=["GET"])
def get_users_search_route():
    search = request.args.get("phrase")
    posts = driver.session().execute_read(get_users_search, search)
    print("Received a GET request on endpoint /api/users/search")
    return {"users": posts}, 200



# GET USER BY USERNAME

def get_user_by_username(tx, username) -> dict:
    query = f"match (u:User) where u.username = \"{username}\" return u"
    results = tx.run(query).data()
    return [{"username": result["u"]["username"], "link": result["u"]["link"], "registered": str(result["u"]["registered"]), "admin": result["u"]["admin"]} for result in results]


@bp_uget.route("/api/users/user/<username>", methods=["GET"])
def get_user_by_username_route(username):
    user = driver.session().execute_read(get_user_by_username, username)
    print(f"Received a GET request on endpoint /api/users/user/{username}")
    return {"user": user[0]}, 200



# GET ACTIVITY OF USER

def get_user_activity(tx, username) -> int:
    exists_check = f"return exists {{match (u:User) where u.username = \"{username}\"}} as ex"
    exists = tx.run(exists_check).data()[0]["ex"]
    if exists:
        query = f"match (u:User)-[:WROTE]-(c:Comment) where u.username = \"{username}\" return count(c) as comments"
        comments = tx.run(query).data()[0]["comments"]
        query2 = f"match (u:User)-[:WROTE]-(c:Comment) return round(count(c)/count(u), 2) as average"
        average = tx.run(query2).data()[0]["average"]
        return round(comments - average, 2)


@bp_uget.route("/api/users/user/<username>/activity", methods=["GET"])
def get_user_activity_route(username):
    score = driver.session().execute_read(get_user_activity, username)
    print(f"Received a GET request on endpoint /api/users/user/{username}/activity")
    if score:
        return {"score": score}, 200
    return {}, 400
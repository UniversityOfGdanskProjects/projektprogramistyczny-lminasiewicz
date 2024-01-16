import os
import re
import sys
from datetime import date
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_upost = Blueprint("bp_upost", __name__)


# POST LOGIN FORM AND LOG USER IN

def post_user_login(tx, login, pwd) -> dict|None:
    query = f"match (u:User) where u.username = \"{login}\" return u.password"
    hashed = tx.run(query).data()[0]["u.password"]
    if check_password(pwd, hashed):
        token = create_token(tx)
        query2 = f"match (u:User) where u.username = \"{login}\" create (a:Authentication {{token: \"{token}\"}})-[:LOGS_IN]->(u)"
        _ = tx.run(query2)
        return {"username": login, "token": token}
    


@bp_upost.route("/api/users/login", methods=["POST"])
def post_user_login_route():
    req = request.json
    login = req["login"]
    pwd = req["password"]
    session_data = driver.session().execute_write(post_user_login, login, pwd)
    print("Received a POST request on endpoint /api/users/login")
    return session_data, 200



# POST SIGNUP FORM AND LOG USER IN

def post_user_signup(tx, username, pwd, link, admin, registered) -> dict|None:
    hashed_pwd = hash_password(pwd)
    query = f"match (u:User) where u.username = \"{username}\" return u"
    results = tx.run(query).data()
    print("results", results)
    if len(results) == 0:
        query2 = f"create (u:User {{username: \"{username}\", password: \"{hashed_pwd}\", link: \"{link}\", admin: {str(admin).lower()}, registered: Date(\"{registered}\")}})"
        _ = tx.run(query2).data()
        print(f"successfully created an account named \"{username}\"")
        return post_user_login(tx, username, pwd)



@bp_upost.route("/api/users/signup", methods=["POST"])
def post_user_signup_route():
    req = request.json
    username = req["username"]
    pwd = req["password"]
    link = f"/users/{username}"
    admin = False
    registered = str(date.today())
    session_data = driver.session().execute_write(post_user_signup, username, pwd, link, admin, registered)
    print(session_data)
    print("Received a POST request on endpoint /api/users/signup")
    if session_data:
        return session_data, 200
    return {}, 200

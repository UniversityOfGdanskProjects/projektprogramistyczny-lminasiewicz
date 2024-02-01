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
        query2 = f"match (u:User) where u.username = \"{login}\" create (a:Authentication {{token: \"{token}\"}})-[:LOGS_IN]->(u) return u.admin"
        admin = tx.run(query2).data()[0]["u.admin"]
        return {"username": login, "token": token, "admin": admin}
    return "Incorrect Password"
    


@bp_upost.route("/api/users/login", methods=["POST"])
def post_user_login_route():
    req = request.json
    login = req["login"]
    pwd = req["password"]
    if re.match("^.{4,16}$", login):
        if re.match ("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,20}$", pwd):
            session_data = driver.session().execute_write(post_user_login, login, pwd)
            print("Received a POST request on endpoint /api/users/login")
            return session_data, 200
        return "Password must be between 5 and 20 characters, contain a lowercase letter, an uppercase letter, and a digit.", 400
    return "Login must be between 4 and 16 characters.", 400



# POST SIGNUP FORM AND LOG USER IN

def post_user_signup(tx, username, pwd, link, admin, registered) -> dict|None:
    hashed_pwd = hash_password(pwd)
    query = f"match (u:User) where u.username = \"{username}\" return u"
    results = tx.run(query).data()
    if len(results) == 0:
        query2 = f"create (u:User {{username: \"{username}\", password: \"{hashed_pwd}\", link: \"{link}\", admin: {str(admin).lower()}, registered: Date(\"{registered}\")}})"
        _ = tx.run(query2).data()
        print(f"successfully created an account named \"{username}\"")
        return post_user_login(tx, username, pwd)
    return {}



@bp_upost.route("/api/users/signup", methods=["POST"])
def post_user_signup_route():
    req = request.json
    username = req["username"]
    pwd = req["password"]
    link = f"/users/{username}"
    admin = False
    registered = str(date.today())
    if re.match ("^.{4,16}$", username):
        if re.match ("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,20}$", pwd):
            session_data = driver.session().execute_write(post_user_signup, username, pwd, link, admin, registered)
            print(session_data)
            print("Received a POST request on endpoint /api/users/signup")
            return session_data, 200
        return "Password must be between 5 and 20 characters, contain a lowercase letter, an uppercase letter, and a digit.", 400
    return "Username must be between 4 and 16 characters.", 400

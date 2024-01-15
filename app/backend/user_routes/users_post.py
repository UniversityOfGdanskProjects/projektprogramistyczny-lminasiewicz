import os
import re
import sys
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_upost = Blueprint("bp_upost", __name__)


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
    session_data = driver.session().execute_read(post_user_login, login, pwd)
    print("Received a POST request on endpoint /api/users/login")
    return session_data, 200
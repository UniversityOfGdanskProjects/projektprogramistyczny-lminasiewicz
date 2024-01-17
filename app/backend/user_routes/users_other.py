import os
import re
import sys
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_uother = Blueprint("bp_uother", __name__)


# PUT EDIT USER INFO


def put_edit_user(tx, token: str, your_username: str, old_username: str, new_username: str, pwd: str) -> str:
    if authenticate_token(tx, token, your_username):
        is_admin = f"match (a:User) where a.admin = true and a.username = \"{your_username}\" return a"
        if len(tx.run(is_admin).data()) > 0 or your_username == old_username:
            query = f"match (u:User) where u.username = \"{old_username}\" set u.username = \"{new_username}\" set u.password = \"{hash_password(pwd)}\""
            _ = tx.run(query)
            return "Operation Successful"
        return "Unauthorized"
    return "Not Logged In"
    


@bp_uother.route("/users/user/<old_username>/edit", methods=["PUT"])
def put_edit_user_route(old_username):
    your_username = request.args.get("username")
    token = request.args.get("token")
    new_username = request.json["username"]
    pwd = request.json["password"]
    result = driver.session().execute_write(put_edit_user, token, your_username, old_username, new_username, pwd)
    print("Received a POST request on endpoint /api/users/logout")
    return result, 200



# DELETE TOKEN, LOG OUT

def delete_user_logout(tx, username, token) -> str:
    if authenticate_token(tx, token, username):
        query = f"match (a:Authentication)-[r:LOGS_IN]-(u:User) where u.username = \"{username}\" detach delete a"
        _ = tx.run(query)
        return "Operation Successful"
    return "Not Logged In"
    


@bp_uother.route("/users/logout", methods=["DELETE"])
def delete_user_logout_route():
    username = request.args.get("username")
    token = request.args.get("token")
    result = driver.session().execute_write(delete_user_logout, username, token)
    print("Received a POST request on endpoint /api/users/logout")
    return result, 200
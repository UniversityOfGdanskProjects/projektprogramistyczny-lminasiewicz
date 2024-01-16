import os
import re
import sys
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_uother = Blueprint("bp_uother", __name__)


# DELETE TOKEN, LOG OUT

def delete_user_logout(tx, username, token) -> dict|None:
    if authenticate_token(tx, token, username):
        query = f"match (a:Authentication)-[r:LOGS_IN]-(u:User) where u.username = \"{username}\" detach delete a"
        _ = tx.run(query)
        return "Operation Successful"
    return "Error"
    


@bp_uother.route("/api/users/logout", methods=["DELETE"])
def delete_user_logout_route():
    username = request.args.get("username")
    token = request.args.get("token")
    result = driver.session().execute_write(delete_user_logout, username, token)
    print("Received a POST request on endpoint /api/users/logout")
    return result, 200
import os
import re
import sys
import datetime
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_cother = Blueprint("bp_cother", __name__)


# PUT EDIT COMMENT

def put_edit_comment(tx, token: str, username: str, content: str, id: int) -> str:
    if authenticate_token(tx, token, username):
        query = f"match (a:User) where a.admin = true match (u:User)-[:WROTE]->(c:Comment) where id(c) = {id} and (u.username = \"{username}\" or a.username = \"{username}\") set c.content = \"{content}\""
        _ = tx.run(query)
        return "Success"
    return "Error"


@bp_cother.route("/api/comments/edit/<int:id>", methods=["PUT"])
def put_edit_comment_route(id):
    username = request.args.get("username")
    token = request.args.get("token")
    content = request.json["content"]
    result = driver.session().execute_write(put_edit_comment, token, username, content, id)
    print(f"Received a POST request on endpoint /api/comments/edit/{id}")
    return result, 200



# DELETE COMMENT

def delete_comment(tx, token: str, username: str, id: int) -> str:
    if authenticate_token(tx, token, username):
        query = f"match (a:User) where a.admin = true match (u:User)-[:WROTE]->(c:Comment) where id(c) = {id} and (u.username = \"{username}\" or a.username = \"{username}\") set c.deleted = true"
        _ = tx.run(query)
        return "Success"
    return "Error"


@bp_cother.route("/api/comments/delete/<int:id>", methods=["DELETE"])
def delete_comment_route(id):
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    result = driver.session().execute_write(delete_comment, token, username, id)
    print(f"Received a DELETE request on endpoint /comments/delete/{id}")
    return result, 200
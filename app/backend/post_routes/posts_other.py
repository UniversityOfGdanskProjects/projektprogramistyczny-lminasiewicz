import os
import re
import sys
import datetime
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_pother = Blueprint("bp_pother", __name__)


# PUT EDIT POST

def put_edit_post(tx, token: str, username: str, title: str, content: str, tags: str, id: int) -> str:
    if authenticate_token(tx, token, username):
        link = f"/posts/{id}"
        query = f"match (p:Post) where id(p) = {id} set p.title = \"{title}\" set p.content = \"{content}\" set p.tags = \"{tags}\" set p.link = \"{link}\""
        _ = tx.run(query)
        return "Successfully Edited Post"
    return "Error"


@bp_pother.route("/posts/edit/<int:id>", methods=["PUT"])
def put_edit_post_route(id):
    username = request.args.get("username")
    token = request.args.get("token")
    req = request.json
    title = req["title"]
    content = req["content"]
    tags = req["tags"]
    result = driver.session().execute_write(put_edit_post, token, username, title, content, tags, id)
    print(f"Received a POST request on endpoint /post/edit/{id}")
    return result, 200



# DELETE POST

def delete_post(tx, token: str, username: str, id: int) -> str:
    if authenticate_token(tx, token, username):
        admin_check = f"match (u:User) where u.username = \"{username}\" return u.admin"
        admin = tx.run(admin_check).data()[0]["u.admin"]
        if admin:
            query = f"match (c:Comment)-[:RESPONDS_TO*]->(p:Post) where id(p) = {id} detach delete c, p"
            _ = tx.run(query)
        return "Post Deleted Successfully"
    return "Error"


@bp_pother.route("/posts/delete/<int:id>", methods=["DELETE"])
def delete_post_route(id):
    username = request.args.get("username")
    token = request.args.get("token")
    result = driver.session().execute_write(delete_post, token, username, id)
    print(f"Received a DELETE request on endpoint /posts/delete/{id}")
    return result, 200

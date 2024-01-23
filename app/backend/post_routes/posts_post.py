import os
import re
import sys
import datetime
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_ppost = Blueprint("bp_ppost", __name__)


# POST A POST ONTO THE WEBSITE

def post_submit(tx, token: str, username: str, title: str, content: str, tags: str) -> str:
    if authenticate_token(tx, token, username):
        if is_admin(tx, username):
            date = datetime.date.today()
            query = f"match (n) return max(id(n)) as m"
            id = int(tx.run(query).data()[0]["m"]) + 1
            link = f"/posts/{id}"
            query2 = f"create (p:Post {{title: \"{title}\", content: \"{content}\", tags: \"{tags}\", date: Date(\"{date}\"), link: \"{link}\"}})"
            _ = tx.run(query2)
            query3 = f"match (u:User) where u.username = \"{username}\" match (p:Post) where id(p) = {id} create (u)-[:WROTE]->(p)"
            _ = tx.run(query3)
            return "Successfully Created Post"
        return "Error"
    return "Error"


@bp_ppost.route("/api/posts/submit", methods=["POST"])
def post_submit_route():
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    req = request.json
    title = req["title"]
    content = req["content"]
    tags = req["tags"]
    result = driver.session().execute_write(post_submit, token, username, title, content, tags)
    print("Received a POST request on endpoint /api/posts/submit")
    return result, 200

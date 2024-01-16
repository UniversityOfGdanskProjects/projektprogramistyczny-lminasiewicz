import os
import re
import sys
import datetime
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_cpost = Blueprint("bp_cpost", __name__)


# POST A COMMENT ONTO THE WEBSITE

def post_comment_submit(tx, token: str, username: str, content: str, under: int) -> str:
    if authenticate_token(tx, token, username):
        date = datetime.date.today()
        query = f"create (c:Comment {{content: \"{content}\", date: Date(\"{date}\")}})"
        _ = tx.run(query)
        query2 = f"match (n) return id(n) order by id(n) desc limit 1"
        id = int(tx.run(query2).data()[0]["id(n)"])
        query3 = f"match (u:User) where u.username = \"{username}\" match (c:Comment) where id(c) = {id} create (u)-[:WROTE]->(c)"
        _ = tx.run(query3)
        query4 = f"match (c:Comment) where id(c)={id} match (x) where id(x)={under} create (c)-[:RESPONDS_TO]->(x)"
        _ = tx.run(query4)
        return "Successfully Created Comment"
    return "Error"


@bp_cpost.route("/comments/submit", methods=["POST"])
def post_comment_submit_route():
    username = request.args.get("username")
    token = request.args.get("token")
    req = request.json
    title = req["content"]
    under = req["under"]
    result = driver.session().execute_write(post_comment_submit, token, username, title, under)
    print("Received a POST request on endpoint /post/submit")
    return result, 200

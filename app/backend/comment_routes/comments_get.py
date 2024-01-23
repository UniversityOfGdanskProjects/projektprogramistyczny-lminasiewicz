import os
import re
import sys
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_cget = Blueprint("bp_cget", __name__)



# GET COUNT OF COMMENTS ON THE WEBSITE

def get_count_comments(tx) -> int:
    query = "match (c:Comment) return count(c)"
    results = tx.run(query).data()
    return results[0]["count(c)"]


@bp_cget.route("/api/comments/count", methods=["GET"])
def get_count_comments_route():
    count = driver.session().execute_read(get_count_comments)
    print("Received a GET request on endpoint /api/comments/count")
    return {"count": count}, 200



# GET COMMENTS BY POST ID OF THE POST THEY'RE UNDER

def get_comments_by_post_id(tx, id: int) -> list[dict]:
    query = f"match (u:User)-[:WROTE]->(c:Comment)-[:RESPONDS_TO]->(p:Post) where id(p) = {id} return u.username, id(c), c"
    results = tx.run(query).data()
    if results:
        return [{"author": result["u.username"], "id": result["id(c)"], "date": str(result["c"]["date"]), "content": result["c"]["content"], "deleted": result["c"]["deleted"]} for result in results]


@bp_cget.route("/api/comments/byPost/<int:id>", methods=["GET"])
def get_comments_by_post_id_route(id: int):
    comments = driver.session().execute_read(get_comments_by_post_id, id)
    print(f"Received a GET request on endpoint /api/comments/byPost/{id}")
    return {"comments": comments}, 200 



# GET COMMENTS BY COMMENT ID OF THE COMMENT THEY'RE UNDER

def get_comments_by_comment_id(tx, id: int) -> list[dict]:
    query = f"match (u:User)-[:WROTE]->(c:Comment)-[:RESPONDS_TO]->(c2:Comment) where id(c2) = {id} return u.username, id(c), c"
    results = tx.run(query).data()
    if results:
        return [{"author": result["u.username"], "id": result["id(c)"], "date": str(result["c"]["date"]), "content": result["c"]["content"], "deleted": result["c"]["deleted"]} for result in results]


@bp_cget.route("/api/comments/byComment/<int:id>", methods=["GET"])
def get_comments_by_comment_id_route(id: int):
    comments = driver.session().execute_read(get_comments_by_comment_id, id)
    print(f"Received a GET request on endpoint /api/comments/byComment/{id}")
    return {"comments": comments}, 200 



# GET COMMENTS BY USERNAME (WITH LINKS TO RELEVANT POST)

def get_comments_by_username(tx, username: str) -> list[dict]:
    query = f"match (u:User)-[:WROTE]->(c:Comment) where u.username = \"{username}\" return c, id(c)"
    results = tx.run(query).data()
    if not results:
        return None
    else:
        def get_link(id):
            query = f"match (c:Comment)-[:RESPONDS_TO*]->(p:Post) where id(c)={id} and c.deleted = false return p.link"
            results = tx.run(query).data()
            return results[0]

        links = list(map(lambda id: get_link(id), [result["id(c)"] for result in results]))
        def rec_merge(comments, links, counter, acc=[]):
            if counter > 0:
                return rec_merge(comments[:-1], links[:-1], counter-1, acc+[{
                    "id": comments[counter-1]["id(c)"], "date": str(comments[counter-1]["c"]["date"]),
                    "content": comments[counter-1]["c"]["content"], "deleted": comments[counter-1]["c"]["deleted"], "original_post": links[counter-1]["p.link"]}])
            else:
                return acc
        
        data = rec_merge(results, links, len(results))
        print(data)
        return data


@bp_cget.route("/api/<username>/comments", methods=["GET"])
def get_comments_by_username_route(username: str):
    comments = driver.session().execute_read(get_comments_by_username, username)
    print(f"Received a GET request on endpoint /api/{username}/comments")
    return jsonify({"comments": comments}), 200
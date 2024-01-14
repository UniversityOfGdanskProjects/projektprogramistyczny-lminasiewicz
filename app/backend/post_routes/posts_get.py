import os
import re
import sys
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_pget = Blueprint("bp_pget", __name__)


# GET ALL POSTS (NO FILTERS)

def get_posts(tx) -> dict:
    query = "match (p:Post) return p, id(p)"
    results = tx.run(query).data()
    if not results:
        return None
    else:
        return [{"id": result["id(p)"], "title": result["p"]["title"], "content": result["p"]["content"], "link": result["p"]["link"], "date": str(result["p"]["date"]), "tags": result["p"]["tags"]} for result in results]


@bp_pget.route("/api/posts", methods=["GET"])
def get_posts_route():
    posts = driver.session().execute_read(get_posts)
    print("Received a GET request on endpoint /api/posts")
    print(jsonify(posts))
    return {"posts": posts}, 200



# GET ALL POSTS (FILTERED WITH TAGS AND DATE)

def get_filtered_posts(tx, tags: list[str], before: str|None = None, after: str = "1970-01-01") -> dict:
    query = f"match (p:Post) where any(tag in p.tags where tag in {tags}) and p.date > Date(\"{after}\") and p.date > Date(\"{before}\") return p"
    if not before:
        query = f"match (p:Post) where any(tag in p.tags where tag in {tags}) and p.date > Date(\"{after}\") return p"
    results = tx.run(query).data()
    return [{"title": result["p"]["title"], "content": result["p"]["content"], "link": result["p"]["link"], "date": str(result["p"]["date"]), "tags": result["p"]["tags"]} for result in results]


@bp_pget.route("/api/posts/filters", methods=["GET"])
def get_filtered_posts_route():
    tags = request.args.get("tags").split(",")
    after = request.args.get("after", "1970-01-01")
    before = request.args.get("before", None)
    print("after:", after)
    if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", after) and (not before or re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", before)):
        posts = driver.session().execute_read(get_filtered_posts, tags, before, after)
        print(f"Received a GET request on endpoint /api/posts/filters with parameters: tags={','.join(tags)} after={after} before={before}")
        return {"posts": posts}, 200
    return None, 400



# GET COUNT OF POSTS ON THE WEBSITE

def get_count_posts(tx) -> int:
    query = "match (p:Post) return count(p)"
    results = tx.run(query).data()
    return results[0]["count(p)"]


@bp_pget.route("/api/posts/count", methods=["GET"])
def get_count_posts_route():
    count = driver.session().execute_read(get_count_posts)
    print("Received a GET request on endpoint /api/posts/count")
    return {"count": count}, 200



# GET POST BY ID

def get_post_by_id(tx, id: int) -> dict:
    query = f"match (p:Post) where id(p) = {id} return p"
    results = tx.run(query).data()
    if results:
        return {"title": results[0]["p"]["title"], "content": results[0]["p"]["content"], "link": results[0]["p"]["link"], "date": str(results[0]["p"]["date"]), "tags": results[0]["p"]["tags"]}


@bp_pget.route("/api/posts/<int:id>", methods=["GET"])
def get_post_by_id_route(id: int):
    post = driver.session().execute_read(get_post_by_id, id)
    print(f"Received a GET request on endpoint /api/posts/{id}")
    return {"post": post}, 200 
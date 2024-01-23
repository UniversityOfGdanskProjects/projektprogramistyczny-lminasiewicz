import os
import re
import sys
from datetime import datetime
from flask import Blueprint, request, jsonify

sys.path.append("..")
from db_connection import driver
from helper_functions import *

bp_other = Blueprint("bp_other", __name__)


# POST SEND MESSAGE TO USER

def post_send_message(tx, token: str, username: str, recipient: str, content: str) -> str:
    if authenticate_token(token, username):
        if recipient:
            exists_query = f"match (u:User) where u.username = \"{recipient}\""
            exists = tx.run(exists_query).data()
            if is_admin(tx, username) and exists:
                time = str(datetime.now())
                query = f"match (u1:User) where u1.username = \"{username}\" match (u2:User) where u2.username = \"{recipient}\" create (m:Message {{content: \"{content}\", posted: datetime(\"{time}\")}}) create (u1)-[:WROTE]->(m)-[:TO]->(u2)"
                _ = tx.run(query)
                return "Message Successfully Sent"
            return "Only Admins can post to any existing user!"
        else:
            time = str(datetime.now())
            query = f"match (u1:User) where u1.username = \"{username}\" match (u2:User) where u2.admin = true create (m:Message {{content: \"{content}\", posted: datetime(\"{time}\")}}) create (u1)-[:WROTE]->(m)-[:TO]->(u2)"
            return "Message Successfully Sent"
    return "Authentication Failure"


@bp_other.route("/api/messages/message", methods=["POST"])
def post_send_message_route():
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    recipient = request.json["recipient"]
    content = request.json["content"]
    status = driver.session().execute_write(post_send_message, token, username, recipient, content)
    print("Received a POST request on endpoint /api/messages/message")
    return status, 200



# GET RECEIVED MESSAGES

def get_received_messages(tx, token: str, username: str, target: str) -> str|list[dict]:
    if authenticate_token(tx, token, username):
        if is_admin(tx, username) or username == target:
            query = f"match (m:Message)-[:TO]->(u:User) where u.username = \"{target}\" return m"
            results = tx.run(query).data()
            return [{"content": result["m"]["content"], "time": result["m"]["time"]} for result in results]
        return "Unauthorized"
    return "Not Logged In"
    


@bp_other.route("/api/messages/get/<target>", methods=["GET"])
def get_received_messages_route(target):
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    results = driver.session().execute_write(get_received_messages, token, username, target)
    print(f"Received a GET request on endpoint /api/messages/get/{target}")
    return {"messages": results}, 200



# POST ADD RATING TO POST

def post_add_rating(tx, token: str, username: str, id: int, rating: int|float) -> str:
    rating = rating // 1
    if rating < 1: rating = 1
    if rating > 5: rating = 5
    if authenticate_token(token, username):
        exists_query = f"match (u:User) where u.username = \"{username}\" match (p:Post) where id(p) = {id} return exists {{ match (u)-[:CREATED]->(:Rating)-[:RATES]->(p) }}"
        exists = tx.run(exists_query).data()
        if not exists:
            today = str(datetime.today())
            query = f"match (u:User) where u.username = \"{username}\" match (p:User) where id(p) = {id} create (r:Rating {{score: \"{rating}\", posted: date(\"{today}\")}}) create (u)-[:CREATED]->(r)-[:RATES]->(p)"
            _ = tx.run(query)
            return "Message Successfully Sent"
        return "Rating already exists."
    return "Not Logged In"


@bp_other.route("/api/posts/<int:id>/review", methods=["POST"])
def post_add_rating_route(id):
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    rating = request.json["rating"]
    status = driver.session().execute_write(post_add_rating, token, username, id, rating)
    print("Received a POST request on endpoint /api/messages/review")
    return status, 200



# GET POST RATING

def get_post_rating(tx, id: int) -> int|None:
    query = f"match (r:Rating)-[:RATES]->(p:Post) where id(p) = {id} return avg(r) as average"
    results = tx.run(query).data()[0]["average"]
    if results:
        return results


@bp_other.route("/api/posts/<int:id>/rating", methods=["GET"])
def get_post_rating_route(id):
    results = driver.session().execute_write(get_post_rating, id)
    print(f"Received a GET request on endpoint /api/posts/{id}/rating")
    return {"messages": results}, 200



# EXPORT POSTS TO CSV AS A BACKUP

def post_backup_posts(tx, username, token) -> str:
    if authenticate_token(tx, token, username):
        if is_admin(tx, username):
            query = f"MATCH (p:Post) WITH collect(p) AS posts CALL apoc.export.csv.data(posts, [], \"posts.csv\", {{}}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file"
            file = tx.run(query).data()
            file.save("../backups/posts.csv")
            return "Operation Successful"
        return "Unauthorized"
    return "Not Logged In"
    


@bp_other.route("/api/backup/posts", methods=["POST"])
def post_backup_posts_route():
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    result = driver.session().execute_write(post_backup_posts, username, token)
    print("Received a POST request on endpoint /api/backup/posts")
    return result, 200



# IMPORT POSTS FROM CSV BACKUP

def post_import_backup_posts(tx, username, token) -> str:
    if authenticate_token(tx, token, username):
        if is_admin(tx, username):
            query = "CALL apoc.import.csv([{fileName: 'file:../backups/posts.csv', labels: ['Post']}], [], {delimiter: '|', arrayDelimiter: ','})"
            _ = tx.run(query).data()
            return "Operation Successful"
        return "Unauthorized"
    return "Not Logged In"
    


@bp_other.route("/api/backup/load/posts", methods=["POST"])
def post_import_backup_posts_route():
    username = request.args.get("username", "")
    token = request.args.get("token", "")
    result = driver.session().execute_write(post_import_backup_posts, username, token)
    print("Received a POST request on endpoint /api/backup/posts")
    return result, 200


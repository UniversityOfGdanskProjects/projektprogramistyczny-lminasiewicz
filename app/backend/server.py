import os
import re
from flask import Flask, request, jsonify
from neo4j import GraphDatabase
from neo4j.time import Date
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
auth = (user, password)
driver = GraphDatabase.driver(uri, auth=auth, database="neo4j")

### ------------ HELPER FUNCTIONS ------------- ###




### ------------ GET ENDPOINTS ------------- ###

# GET ALL NODES

def get_data(tx) -> dict:
    query = "match (n) return n"
    results = tx.run(query).data()
    if not results:
        return None
    else:
        data = [result["n"] for result in results]
        print(data)
        return data


@app.route("/api/db", methods=["GET"])
def get_data_route():
    print("Received a GET request on endpoint /api/db")
    data = driver.session().execute_read(get_data)
    if data:
        return jsonify(data), 200
    else:
        return {}, 200


# GET ALL POSTS (NO FILTERS)

def get_posts(tx) -> dict:
    query = "match (p:Post) return p"
    results = tx.run(query).data()
    if not results:
        return None
    else:
        return [{"title": result["p"]["title"], "content": result["p"]["content"], "link": result["p"]["link"], "date": str(result["p"]["date"]), "tags": result["p"]["tags"]} for result in results]


@app.route("/api/posts", methods=["GET"])
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


@app.route("/api/posts/filters", methods=["GET"])
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


# GET ALL USERS

def get_users(tx) -> list[dict]:
    query = "match (u:User) return u"
    results = tx.run(query).data()
    return results


@app.route("/api/users", methods=["GET"])
def get_users_route():
    posts = driver.session().execute_read(get_users)
    print("Received a GET request on endpoint /api/users")
    return {"posts": jsonify(posts)}, 200


# GET USERNAME & EMAIL VERIFICATION

def get_verification(tx, username: str = "", email: str = "") -> bool:
    query = f"match (u:User) where u.email = \"{email}\" or u.username = \"{username}\" return u"
    if username == "" and email == "":
        return False
    results = tx.run(query).data()
    if len(results) == 0:
        return True
    else:
        return False


@app.route("/api/verify", methods=["GET"])
def get_verification_route():
    username = request.args.get("username", "")
    email = request.args.get("email", "")
    available = driver.session().execute_read(get_verification, username, email)
    print(f"Received a GET request on endpoint /api/verify with parameters: username=\"{username if username!='' else '<default:none>'}\" email=\"{email if email!='' else '<default:none>'}\" ")
    return {"verification": available}, 200


# GET COMMENTS BY USERNAME (WITH LINKS TO RELEVANT POST)

def get_comments_by_username(tx, username: str) -> list[dict]:
    query = f"match (u:User)-[:WROTE]->(c:Comment) where u.username = \"{username}\" return c, id(c)"
    results = tx.run(query).data()
    if not results:
        return None
    else:
        def get_link(id):
            query = f"match (c:Comment)-[:RESPONDS_TO*]->(p:Post) where id(c)={id} return p.link"
            results = tx.run(query).data()
            return results[0]

        links = list(map(lambda id: get_link(id), [result["id(c)"] for result in results]))
        def rec_merge(comments, links, counter, acc=[]):
            if counter > 0:
                return rec_merge(comments[:-1], links[:-1], counter-1, acc+[{
                    "id": comments[counter-1]["id(c)"], "date": comments[counter-1]["c"]["date"],
                    "content": comments[counter-1]["c"]["content"], "original_post": links[counter-1]["p.link"]}])
            else:
                return acc
        
        data = rec_merge(results, links, len(results))
        print(data)
        return data


@app.route("/api/<username>/comments", methods=["GET"])
def get_comments_by_username_route(username: str):
    comments = driver.session().execute_read(get_comments_by_username, username)
    print(f"Received a GET request on endpoint /api/{username}/comments")
    return jsonify({"comments": comments}), 200


# GET COUNT OF COMMENTS ON THE WEBSITE

def get_count_comments(tx) -> int:
    query = "match (c:Comment) return count(c)"
    results = tx.run(query).data()
    return results


@app.route("/api/comments/count", methods=["GET"])
def get_count_comments_route():
    count = driver.session().execute_read(get_count_comments)
    print("Received a GET request on endpoint /api/comments/count")
    return {"count": count}, 200


# GET COUNT OF REGISTERED USERS

def get_count_users(tx) -> int:
    query = "match (u:Users) return count(u)"
    results = tx.run(query).data()
    return results


@app.route("/api/users/count", methods=["GET"])
def get_count_users_route():
    count = driver.session().execute_read(get_count_users)
    print("Received a GET request on endpoint /api/users/count")
    return {"count": count}, 200









if __name__ == "__main__":
    app.run()
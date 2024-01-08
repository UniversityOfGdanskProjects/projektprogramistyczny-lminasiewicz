import os
from flask import Flask, jsonify
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
auth = (user, password)
driver = GraphDatabase.driver(uri, auth=auth, database="neo4j")


### ------------ GET ENDPOINTS ------------- ###

# GET ALL NODES

def get_data(tx):
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

def get_posts(tx):
    query = "match (p:Post) return p"
    results = tx.run(query).data()
    if not results:
        return None
    else:
        return results


@app.route("/api/posts", methods=["GET"])
def get_posts_route():
    posts = driver.session().execute_read(get_posts)
    print("Received a GET request on endpoint /api/posts")
    return {"posts": jsonify(posts)}, 200


# GET ALL POSTS (FILTERED WITH TAGS AND DATE)

#def get_filtered_posts(tx, tags: list[str], before: str|None, after: str|None):



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
                return rec_merge(comments[:-1], links[:-1], counter-1, 
                                 acc+[{"id": comments[counter-1]["id(c)"], "date": comments[counter-1]["c"]["date"],
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






if __name__ == "__main__":
    app.run()
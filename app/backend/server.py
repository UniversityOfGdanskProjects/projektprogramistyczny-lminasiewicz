import re
from flask import Flask, request, jsonify
from db_connection import driver
from helper_functions import *

app = Flask(__name__)

from post_routes.posts_get import bp_pget
from post_routes.posts_post import bp_ppost
from post_routes.posts_other import bp_pother
from comment_routes.comments_get import bp_cget
from comment_routes.comments_post import bp_cpost
from comment_routes.comments_other import bp_cother
from user_routes.users_get import bp_uget
from user_routes.users_post import bp_upost
from user_routes.users_other import bp_uother
from other_routes.other_routes import bp_other


app.register_blueprint(bp_pget)
app.register_blueprint(bp_ppost)
app.register_blueprint(bp_pother)
app.register_blueprint(bp_cget)
app.register_blueprint(bp_cpost)
app.register_blueprint(bp_cother)
app.register_blueprint(bp_uget)
app.register_blueprint(bp_upost)
app.register_blueprint(bp_uother)
app.register_blueprint(bp_other)


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





if __name__ == "__main__":
    app.run()
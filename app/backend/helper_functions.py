from bcrypt import hashpw, gensalt, checkpw

### ------------ HELPER FUNCTIONS ------------- ###

def authenticate_token(tx, token: str, username: str) -> bool:
    query = f"match (a:Authentication)-[:LOGS_IN]-(u:User) where a.token = \"{token}\" and u.username = \"{username}\" return u"
    results = tx.run(query).data()
    if len(results) <= 0:
        return False
    else:
        return True


def create_token(tx) -> str:
    unique = False
    while not unique:
        query = "call apoc.create.uuids(1)"
        results = tx.run(query).data()[0]["uuid"]
        query2 = "match (a:Authentication) return a.token"
        results2 = tx.run(query2).data()
        if len(results2) != 0:
            parsed_results2 = [result["a.token"] for result in results2]
            if results not in parsed_results2:
                unique = True
        else:
            unique = True
    return results


def delete_token(tx, token) -> None:
    query = f"match (a:Authentication) where a.token = \"{token}\" delete a"
    results = tx.run(query).data()


def hash_password(pwd: str) -> str:
    return hashpw(pwd.encode("utf-8"), gensalt())


def check_password(pwd: str, hashed: str) -> bool:
    return checkpw(pwd.encode("utf-8"), hashed[2:-1].encode("utf-8"))
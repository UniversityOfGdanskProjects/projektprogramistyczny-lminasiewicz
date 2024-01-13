### ------------ HELPER FUNCTIONS ------------- ###

def authenticate_token(tx, token: str, username: str) -> bool:
    query = f"match (a:Authentication)-[:LOGS_IN]-(u:User) where a.token = \"{token}\" and u.username = \"{username}\" return u"
    results = tx.run(query).data()
    if len(results) <= 0:
        return False
    else:
        return True
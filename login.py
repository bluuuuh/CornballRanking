import json
import os
import random
import uuid


def log_in(username, password):
    if os.path.exists("logins.json"):
        with open("logins.json", "r") as file:
            logins = json.load(file)

    if username in logins:
        if (logins.get(username))[0] == password:
            n = logins.get(username)
            return n[1]
    return "Failed"

def create_account(username, password):
    if os.path.exists("logins.json"):
        with open("logins.json") as file:
            logins = json.load(file)

    ID_token = uuid.uuid4().hex

    if username not in logins:
        logins.update({username: [password, ID_token]})
        with open("logins.json", "w") as f:
            json.dump(logins, f)
            return ID_token
    else:
        return "Failed"


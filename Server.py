import json, requests
from flask import Flask, jsonify
from threading import Thread as Threads

def Json(Input , Name):
  with requests.Session() as Session:
    Info = json.loads(Session.get(Input).text)[Name]
    return Info

Server = Flask("RoFind")

@Server.route("/<method>/<input>")
def Index(method, input):
    if method == "rover":
        try:
            UserID = Json(f"https://verify.eryn.io/api/user/{input}", "robloxId")
        except:
            return jsonify({"error": "unknown user"})
    elif method == "bloxlink":
        try:
            UserID = Json(f"https://api.blox.link/v1/user/{input}", "primaryAccount")
        except:
            return jsonify({"error": "unknown user"})
    else:
        return jsonify({"error": "unknown method"})
    Username = Json(f"https://users.roblox.com/v1/users/{UserID}", "name")
    DisplayName = Json(f"https://users.roblox.com/v1/users/{UserID}", "displayName")
    Following = Json(f"https://friends.roblox.com/v1/users/{UserID}/followings/count", "count")
    Followers = Json(f"https://friends.roblox.com/v1/users/{UserID}/followers/count", "count")
    Description = Json(f"https://users.roblox.com/v1/users/{UserID}", "description")
    Status = Json(f"https://api.roblox.com/users/{UserID}/onlinestatus", "LastLocation")
    LastOnlineRaw = Json(f"https://api.roblox.com/users/{UserID}/onlinestatus", "LastOnline")
    Date, Time = LastOnlineRaw.replace("-", "/").split("T")
    LastOnline, Extra = Time.split(".")
    CreatedRaw = Json(f"https://users.roblox.com/v1/users/{UserID}", "created")
    Icon = f"https://www.roblox.com/headshot-thumbnail/image?userId={UserID}&width=720&height=720&format=png"
    Created, Time2 = CreatedRaw.replace("-", "/").split("T")
    Info = {
        "id": f"{UserID}",
        "username": Username,
        "display": DisplayName,
        "following": Following,
        "followers": Followers,
        "status": Status,
        "lastOnline": LastOnline,
        "created": Created,
        "avatarIcon": Icon,
        "description": Description}
    return jsonify(Info)

def Host():
    Server.run(host = "0.0.0.0", port = 8080)

def UpTime():
    Server = Threads(target = Host)
    Server.start()

UpTime()

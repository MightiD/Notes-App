from flask import Flask, request
from datetime import datetime
import json
import os

saveFolder = "./Notes"

app = Flask(__name__)


def getLastID():
    files = os.listdir(saveFolder)
    if len(files) < 1:
        return 0
    
    files.sort()
    file = files[-1]
    ret = file.split(".")[0]
    return int(ret)


@app.route("/api/v1/writeNote", methods=["POST"])
def writeNote():
    content_type = request.headers.get("Content-Type")

    if content_type == "application/json":

        content = request.json

        newID = getLastID() + 1

        saveData = {
            "noteID": newID,
            "timeCreated": f"{datetime.now()}",
            "lastModified": f"{datetime.now()}",
            "content": content["Content"]
        }

        print(saveData)

        #Save file
        with open(f"{saveFolder}/{newID}.json", "w") as f:
            json.dump(saveData, f, ensure_ascii=False, indent=4)
        return saveData

    else:
        return "Content-Type not supported!"


@app.route("/api/v1/getNote/<noteID>")
def getNote(noteID):
    try:
        with open(f"{saveFolder}/{noteID}.json", "r") as file:
            data = json.load(file)
            print(data)
            return data
    except:
        return("Error opening note")


@app.route("/api/v1/getAllNotes")
def getAllNotes():
    files = os.listdir(saveFolder)
    notes = []
    for i in files:
        noteID = (i.split(".")[0])
        notes.append(getNote(noteID))
    return notes

from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

app = Flask(__name__)

client = MongoClient("mongodb+srv://evuser:strongpassword@cluster0.yowawz6.mongodb.net/?appName=Cluster0")

db = client.ev_db
collection = db.vehicles


@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    data = request.json

    coll = collection.with_options(
        write_concern=WriteConcern(w=1)
    )

    result = coll.insert_one(data)

    return jsonify(str(result.inserted_id))


@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    data = request.json

    coll = collection.with_options(
        write_concern=WriteConcern(w="majority")
    )

    result = coll.insert_one(data)

    return jsonify(str(result.inserted_id))


@app.route("/count-tesla-primary")
def count_tesla():

    count = collection.with_options(
        read_preference=ReadPreference.PRIMARY
    ).count_documents({"Make": "TESLA"})

    return jsonify({"count": count})
    
@app.route("/count-bmw-secondary")
def count_bmw():
    count = collection.with_options(
        read_preference=ReadPreference.SECONDARY_PREFERRED
    ).count_documents({"Make": "BMW"})
    return jsonify({"count": count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
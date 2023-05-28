from flask import Flask, render_template, request, jsonify, escape
from pymongo import MongoClient

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("MONGODB_URL")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(DB_HOST)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': escape(bucket_receive),
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    data = list(db.bucket.find({}, {'_id':False}))
    return jsonify({'buckets': data})

@app.route("/bucket/del", methods=["POST"])
def bucket_delete():
    num_receive = int(request.form['num_give'])
    db.bucket.delete_one({'num': num_receive})
    return jsonify({'msg': 'data berhasil di hapus'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

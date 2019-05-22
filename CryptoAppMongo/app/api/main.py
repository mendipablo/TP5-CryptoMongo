import pymongo
from flask import Flask, jsonify, render_template,request,redirect,url_for
from bson.json_util import dumps

def get_db_connection(uri):
    client = pymongo.MongoClient(uri)
    return client.cryptongo

app = Flask(__name__)
connection = get_db_connection('mongodb://mongo-crypto:27017/')

def get_documents():
    params = {}
    name = request.args.get('name', '')
    limit = request.args.get('limit', 0)
    if name:
        params.update({'name': name})
    cursor = connection.data.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)
    return list(cursor)

def get_first():
    params = {}
    name = request.args.get('name', '')
    if name:
        params.update({'name': name})
    cursor = connection.data.find(params, {'_id': 0, 'ticker_hash': 0}).limit(1)
    return list(cursor)

def get_top20():
    params = {}
    name = request.args.get('name', '')
    if name:
        params.update({'name': name})
    
    cursor = connection.data.find(params, {'_id': 0, 'ticker_hash': 0}).limit(20)
    return list(cursor)



@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    t = "HISTORICO"
    documents = get_documents()
    
    return render_template('all.html',documents=documents,t=t)

@app.route('/top')
def topv():
    t = "TOP 20"
    documents = get_top20()
    
    return render_template('top.html',documents=documents,t=t)

@app.route('/one')
def first():
    t = "TOP 1"
    documents = get_first()
    
    return render_template('one.html',documents=documents,t=t)

@app.route('/search', methods=['GET'])
def search():
    key=request.values.get("key")
    documents = connection.data.find({'name':key}).limit(1)
    return render_template('one.html',documents=documents)

@app.route('/remove', methods=['GET','POST'])
def remove():
    
    key=request.args.get("key")
    connection.data.delete_many({'name':key})
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
   

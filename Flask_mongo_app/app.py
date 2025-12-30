from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi 
import json

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)


ca = certifi.where()
MONGO_URI = "mongodb+srv://Madhav06:BARCELONA@cluster0.gxxrv6r.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=ca
)
db = client["flask_db"]
collection = db["users"]

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            collection.insert_one({
                "name": name,
                "email": email
            })

            return redirect(url_for('success'))

        except Exception as e:
            error = str(e)

    return render_template('index.html', error=error)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)

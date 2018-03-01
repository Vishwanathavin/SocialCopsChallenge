from flask import Flask,g,jsonify,request
from flask_pymongo import PyMongo

app = Flask(__name__)


app.config.from_object('config')

mongo = PyMongo(app)

# THis is needed to give global access to the db and be able to put values in the db
@app.before_request
def before_request():
    g.db = mongo.db

@app.route('/')
def index():
    #response = jsonify({"Message":"Welcome to YNOS"});
    #response.headers.add('Access-Control-Allow-Origin', '*');
    return jsonify({"Message":"Welcome to Social Cops : APMC commodity prices main page"})


@app.route('/actualPrices/<APMC>/<COMMODITY>',methods=['GET'])
def stationaryPrices(APMC,COMMODITY):
    salesDetails = g.db.APMC.find_one({"$and":[{"Name":APMC},{"commodityList":{"$elemMatch":{"Name":COMMODITY}}}]},{"commodityList.$":1})

    return jsonify({"Details": salesDetails})

@app.route('/stationaryPrices/<APMC>/<COMMODITY>',methods=['GET'])
def stationaryPrices(APMC,COMMODITY):
    salesDetails = g.db.APMC.find_one({"$and":[{"Name":APMC},{"commodityList":{"$elemMatch":{"Name":COMMODITY}}}]},{"commodityList.$":1})

    return jsonify({"Details": salesDetails})


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
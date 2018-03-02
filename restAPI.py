from flask import Flask,g,jsonify,request
from flask_pymongo import PyMongo
from algorithm import stationarity,getFluctuation
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
def actualPrices(APMC,COMMODITY):
    salesDetails = g.db.APMC.find_one({"$and":[{"Name":APMC},{"commodityList":{"$elemMatch":{"Name":COMMODITY}}}]},{"commodityList.$":1})

    return jsonify({"Details": salesDetails})

@app.route('/stationaryPrices/<APMC>/<COMMODITY>',methods=['GET'])
def stationaryPrices(APMC,COMMODITY):
    salesDetails = g.db.APMC.find_one({"$and":[{"Name":APMC},{"commodityList":{"$elemMatch":{"Name":COMMODITY}}}]},{"commodityList.$":1})
    # print (salesDetails["commodityList"])
    # print (salesDetails["commodityList"][0]["salesList"])
    stationaryData = stationarity(salesDetails["commodityList"][0]["salesList"])
    stationaryData = stationaryData.to_dict('records')
    return jsonify({"stationaryData": stationaryData})

@app.route('/calculateFluctuation',methods=['GET'])
def calFluctuation():
    salesDetails = g.db.APMC.find()
    flucData = getFluctuation(list(salesDetails))

    flucData.set_index(['APMC', 'Commodity', 'date'], inplace=True)
    for idone, APMC in flucData.groupby('APMC'):
        APMCdetails = {"Name": idone, "commodityList": []}

        for idtwo, commodity in APMC.groupby('Commodity'):
            commoditydetails = {"Name": idtwo, "salesList": []}
            for idthree, date in commodity.groupby('date'):
                dateDetails = {"date": idthree, "fluc": float(date['fluc'].values[0])}
                commoditydetails['salesList'].append(dateDetails)
            APMCdetails["commodityList"].append(commoditydetails)
        g.db.APMCFluc.update({"_id": APMCdetails["Name"]}, {'$set': APMCdetails}, upsert=True)


    # flucData = flucData.to_dict('records')

    return jsonify({"message":"fluctuation detail calculated for the current dataset"})

@app.route('/fluctuation/<number>',methods=['GET'])
def getFluctuation(number):

    output=number
    return jsonify({"Top fluctutations":output})


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
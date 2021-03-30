from flask import Flask, jsonify
from flask_cors import cross_origin
import stock

app = Flask(__name__)

@app.route("/api/ParseChipData/GroupByBroker/")
@cross_origin()
def GroupByBroker():
    chipData = stock.GroupByBroker()
    return chipData

@app.route("/api/ParseChipData/GroupByPrice/")
@cross_origin()
def GroupByPrice():
    chipData = stock.GroupByPrice()
    return chipData
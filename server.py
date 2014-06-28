from flask import Flask, request
from datetime import datetime
app = Flask(__name__)
outputFile = open("dataset.csv", 'w')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/loggerdata", methods=["POST"])
def loggerData():
	if request.method == "POST":
		date = datetime.now();
		sdate = date.strftime('%Y-%m-%d %H-%M:%S.%f');
		timestamp = request.form["timestamp"];
		value = request.form["value"];
		print timestamp;
		print value;
		outputFile.write("%s,%s\n" % (sdate, value));
		return "ok";
	else:
		app.logger.error('Not a POST method');
		return "error";

if __name__ == "__main__":
    app.run(host="0.0.0.0")


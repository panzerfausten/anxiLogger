from flask import Flask, request
from datetime import datetime
app = Flask(__name__)

class AnxiServer():
	def __init__(self,mode,outputfile = None,port=5000):
		self.mode = mode
		self.port = port
		self.isLogging = False
		#if no path is specified, no data is saved
		if(outputfile != None):
			self.isLogging = True
			self.outputFile = open(outputfile, 'w')
	def start(self):
    		app.run(host="0.0.0.0",port=self.port, debug=True)
@app.route("/")
def dispatch_request():
	return str (_ANXISERVER.isLogging ) 


@app.route("/api/loggerdata", methods=["POST"])
def loggerData():
	if request.method == "POST":
		date = datetime.now();
		sdate = date.strftime('%Y-%m-%d %H-%M:%S.%f');
		timestamp = request.form["timestamp"];
		value = request.form["value"];
		print timestamp;
		print value;
		_ANXISERVER.outputFile.write("%s,%s\n" % (sdate, value));
		_ANXISERVER.outputFile.flush()
		return "ok";
	else:
		app.logger.error('Not a POST method');
		return "error";

if __name__ == "__main__":
	_ANXISERVER = AnxiServer("ANXI","test.csv");
	_ANXISERVER.start()

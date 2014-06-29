from flask import Flask, request
from datetime import datetime
import sys
app = Flask(__name__)

class AnxiServer():
	def __init__(self,mode,outputfile = None,port=5000):
		self.mode = mode
		self.port = port
		self.outputfile= outputfile
		self.isLogging = False
		self.lastValue = -999
		#if no path is specified, no data is saved
		if(outputfile != None):
			self.isLogging = True
			if (self.mode == "SAMPLE"):
				self.OUTPUT_FILE_PATH = self.outputfile + "IR_SAMPLE" + datetime.now().strftime('%Y%m%d%H%M%S')  + ".csv"
			else:
				self.OUTPUT_FILE_PATH = self.outputfile +  "IR" + datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
			
			self.outputFile = open(self.OUTPUT_FILE_PATH, 'w')
	def start(self):
    		app.run(host="0.0.0.0",port=self.port, debug=False)
	def stop(self):
		if(self.isLogging):
			#close file
			self.outputFile.close()
			func = request.environ.get('werkzeug.server.shutdown')
			if func is None:
				raise RuntimeError('Not running with the Werkzeug Server')
			func()
@app.route("/")
def dispatch_request():
	_ANXISERVER.stop()
	#return str (_ANXISERVER.isLogging ) 
	return "Stoping server"
@app.route("/api/glass/1/irvalue")
def irvalue():
	return str( _ANXISERVER.lastValue)

@app.route( "/api/mode", methods= ["GET","POST"] )
def modes():
	if request.method == "GET":
		return _ANXISERVER.mode
	elif reqiest.method == "POST":
		_ANXISERVER.mode = request.form["mode"]
		return "1"
@app.route("/api/loggerdata", methods=["POST"])
def loggerData():
	if request.method == "POST":
		date = datetime.now();
		sdate = date.strftime('%Y-%m-%d %H-%M:%S.%f');
		value = request.form["value"];
		_ANXISERVER.lastValue  =  value
		print value;
		_ANXISERVER.outputFile.write("%s,%s, %s\n" % (sdate, _ANXISERVER.mode,value));
		_ANXISERVER.outputFile.flush()
		return "ok";
	else:
		app.logger.error('Not a POST method');
		return "error";

if __name__ == "__main__":
	try:
		_MODE = sys.argv[1]
		_FILE = sys.argv[2]
		_ANXISERVER = AnxiServer(_MODE,_FILE);
		_ANXISERVER.start()
    	except:
		print "You must specify a MODE and a FILE"
		sys.exit(1)


import serial
import platform
import curses
import zephyr
from zephyr.testing import simulationWorkflow
from datetime import datetime
import sys
import signal
import csv
from curses import wrapper

class MeasureHearthRate:
	def __init__(self,OUTPUT_FILE_PATH = None,mode="ANXIETY_INDUCTION",sampleTime=300):
		self.initDateTime = datetime.now()
		self.sw = simulationWorkflow()
		#in seconds
		self.sampleTime = sampleTime
		#sets if saving to file is needed
		self.isSavingtoFile = False
		self.mode = mode
		#if no path is specified, no data is saved
		if (OUTPUT_FILE_PATH != None):
			#takes specified PATH and appends extra info
			self._OUTPUT_FILE_PATH =  OUTPUT_FILE_PATH
			#if is a sample dataset, we append _sample_
			if (self.mode =="SAMPLE"):
				self._OUTPUT_FILE_PATH += "_SAMPLE_"
			#adds timestamp
			self._OUTPUT_FILE_PATH += "_"+datetime.now().strftime('%Y%m%d%H%M%S')
			#opens output file
			self._OUTPUT_FILE = open(self._OUTPUT_FILE_PATH +".csv", 'w')
			#we are saving to disk!
			self.isSavingtoFile = True
	def callback(self,value_name, value):
		#takes stamptime for each row
    		date = datetime.now()
		sdate = date.strftime('%Y-%m-%d %H-%M:%S')
		#displays data only when heart_rate is reported
		if(value_name == "heart_rate"):
			self.stdscr.move(2,0)
			#uses curses to display data
			#display timings
			self.stdscr.deleteln()
			self.stdscr.deleteln()
			self.stdscr.deleteln()
			self.stdscr.addstr("Start time: %s. Elapsed Time: %s seconds." %
						(self.initDateTime.strftime('%Y-%m-%d %H:%M:%S'),  (date -self.initDateTime).seconds
						))
			self.stdscr.addstr(   "MODE:%s.\n" % self.mode , curses.color_pair(1))

			self.stdscr.addstr("HR:%s" %( str(value)))	
			self.stdscr.refresh()
			c = self.stdscr.getch()
			#sets controls in interactive console
			if (c == ord('q')):
				self.terminate()
			#gets you into relaxation state
			if (self.mode != "SAMPLE"):
				if (c == ord('r')):
					self.mode = "RELAXATION"
		#save it to file
		if(self.isSavingtoFile):
			self._OUTPUT_FILE.write("%s,%s,%s,%s\n"  % (sdate,self.mode,value_name,str(value)))
		#break if we are in sample mode
		if(   (date - self.initDateTime).seconds >= self.sampleTime):
			self.terminate()
	def terminate(self):
		#self.ser.close()
		self.sw.terminate()
	#Initialazes the devices
	def main(self):
    		serial_port_dict = {"Darwin": "/dev/tty.HXM026692-BluetoothSeri",
                        "Windows": 23}
    		serial_port = serial_port_dict[platform.system()]
    		self.ser = serial.Serial(serial_port)
 		self.sw.simulation_workflow([self.callback], self.ser)	
	#to use it with curses 
	def startCurse(self,stdscr):
		self.stdscr = stdscr
		self.stdscr.nodelay(True)
		stdscr.clear()
		if(self.mode == "ANXIETY_INDUCTION"):
			self.stdscr.addstr("Press [r] to change to RELAXATION MODE. Press [q] to exit\n")
		else:
			self.stdscr.addstr("SAMPLE MODE. Program will exit after %i seconds. Press [q] to exit\n" % self.sampleTime)
		
		self.stdscr.refresh()
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        	mhr.main()
def usage():
	print "USAGE: python read_from_device.py [OPTIONS] [outputfile]"
	print "OPTIONS:"
	print "		--nolog: avoids saving to disk"
	print "		--sample: Takes a sample of 5 minutes of data"
	print "EXAMPLE:"
	print "		Running in sample mode"
	print "		python anxiLogger.py --sample logs/subject"
	print ""
	print "		Running in ANXIETY INDUCTION  mode"
	print "		python anxiLogger.py logs/subject"
	print ""
	print ""
	print "Darien Miranda <dmiranda@cicese.edu.mx>"
	

if __name__ == "__main__":
    try:
	argv1 = sys.argv[1]
    except:
	usage()
	sys.exit(1)
    if (argv1 == "--nolog"):
        mhr = MeasureHearthRate()
    elif (argv1 == "--sample"):
	try:
		argv2 = sys.argv[2]
	except:
		print "You must specify an output file"
		sys.exit(1)
	mhr = MeasureHearthRate(argv2,mode="SAMPLE")
    else:
        mhr = MeasureHearthRate(argv1)
    wrapper(mhr.startCurse)

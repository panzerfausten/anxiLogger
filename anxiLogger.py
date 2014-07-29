import serial
import requests
import platform
import curses
import zephyr
from zephyr.testing import simulationWorkflow
from datetime import datetime
import sys
import signal
import csv
from curses import wrapper
#Google glass server
from AnxiServer import AnxiServer
import os 
class AnxiLoggerApp:
	#sample time in seconds
	def __init__(self,OUTPUT_FILE_PATH = None,mode="ANXIETY_INDUCTION",sampleTime=300):
		self.initDateTime = datetime.now()
		self.platform = platform.system()[0]
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
			#if is a sample mode, we append _sample_
			if (self.mode =="SAMPLE"):
				self._OUTPUT_FILE_PATH += "_SAMPLE_"
			#adds timestamp
			self._OUTPUT_FILE_PATH += "_"+datetime.now().strftime('%Y%m%d%H%M%S')
			#self._OUTPUT_IR_FILE_PATH = self.OUTPUT_FILE_PATH 
			#opens output file
			self._OUTPUT_FILE = open(self._OUTPUT_FILE_PATH +".csv", 'w')
			#we are saving to disk!
			self.isSavingtoFile = True
		self._ANXY_SERVER = AnxiServerClient()
	def updateUI(self,x,y,value):
    		date = datetime.now()
			#uses curses to display data
		self.stdscr.move(2,0)
		self.stdscr.deleteln()
		self.stdscr.deleteln()
		self.stdscr.addstr("Start time: %s. Elapsed Time: %s seconds." %
					(self.initDateTime.strftime('%Y-%m-%d %H:%M:%S'),  (date -self.initDateTime).seconds
					))
		self.stdscr.addstr("MODE:%s.\n" % self.mode , curses.color_pair(1))
		self.stdscr.addstr(value + "\n")
		
		#TODO: Do it better, i don't feel like doing it by myself
		_irValue = self._ANXY_SERVER.getIRValue()
		self.stdscr.addstr("IRSensor:%s" % str(_irValue))
		self.stdscr.refresh()
		c = self.stdscr.getch()
		#sets controls in interactive console
		if (c == ord('q')):
			self.terminate()
		#gets you into relaxation state
		if (self.mode != "SAMPLE"):
			if (c == ord('r')):
				self.mode = "RELAXATION"
				self._ANXY_SERVER.setMode("RELAXATION")
	def callbackZephyr(self,value_name, value):
		#takes stamptime for each row
    		date = datetime.now()
		sdate = date.strftime('%Y-%m-%d %H-%M:%S')
		#displays data only when heart_rate is reported
		if(value_name == "heart_rate"):
			self.updateUI(2,0,"HR:%s" %( str(value)))
		#save it to file TODO:MOVE THIS TO A LOG METHOD
		if(self.isSavingtoFile):
			self._OUTPUT_FILE.write("%s,%s,%s,%s\n"  % (sdate,self.mode,value_name,str(value)))
		#break if we are in sample mode
		if(   (date - self.initDateTime).seconds >= self.sampleTime  and self.mode =="SAMPLE"):
			self.terminate()
	def terminate(self):
		#self.ser.close()
		self.sw.terminate()
	#Initialazes the devices
	def main(self):
			#START ZEPYRH BT
			serial_port_dict = {"Darwin": "/dev/tty.HXM026692-BluetoothSeri",
					"Linux": "/dev/rfcomm0",
					"Windows": 23}
			serial_port = serial_port_dict[platform.system()]
			self.ser = serial.Serial(serial_port)
			self.sw.simulation_workflow([self.callbackZephyr], self.ser)
			#START GOOGLE GLASS
	#to use it with curses 
	def startCurse(self,stdscr):
		self.stdscr = stdscr
		self.stdscr.nodelay(True)
		stdscr.clear()
		if(self.mode == "ANXIETY_INDUCTION"):
			self.stdscr.addstr("Press [r] to change to RELAXATION MODE. Press [q] to exit\n")
		elif(self.mode == "SAMPLE"):
			self.stdscr.addstr("SAMPLE MODE. Program will exit after %i seconds. Press [q] to exit\n" % self.sampleTime)
		elif(self.mode == "NOLOG"):
			self.stdscr.addstr("NOLOG MODE. Program will not save any data to disk. Press [q] to exit\n")
		self.stdscr.refresh()
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        	mhr.main()
class AnxiServerClient:
	def __init__(self):
		#Set AnxiServerDATA
		self.ANXISERVER_IR_VALUE_URL = "http://0.0.0.0:5000/api/glass/1/irvalue"
		self.ANXISERVER_MODE_URL= "http://0.0.0.0:5000/api/mode"
	def getIRValue(self):
		irValue = -99999999999999999
		#try:
			#r = requests.get(self.ANXISERVER_IR_VALUE_URL)
			#irValue = float( r.text)
		#except:
		#	return irValue
		
		return irValue
	def setMode(self,mode):
		try:
			r = requests.post(self.ANXISERVER_MODE_URL)
		except:
			pass
	
			
	
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
	
def license():
    print "AnxiLogger  Copyright (C) 2014  Darien Miranda"
    print "This program comes with ABSOLUTELY NO WARRANTY."
    print "This is free software, and you are welcome to redistribute it"
    print "under certain conditions."
if __name__ == "__main__":
    license()
    try:
	argv1 = sys.argv[1]
    except:
	usage()
	sys.exit(1)
    if (argv1 == "--nolog"):
        mhr = AnxiLoggerApp(mode="NOLOG")
    elif (argv1 == "--sample"):
	try:
		argv2 = sys.argv[2]
	except:
		print "You must specify an output file"
		sys.exit(1)
	print "starting sample"
	mhr = AnxiLoggerApp(argv2,mode="SAMPLE")
    else:
        mhr = AnxiLoggerApp(argv1)
    wrapper(mhr.startCurse)

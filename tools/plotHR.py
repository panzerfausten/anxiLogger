import sys

try:
	_FILE_PATH = sys.argv[1]
	_SUBJECT_NAME = sys.argv[2]
	_OUTPUT_FIG_PATH = sys.argv[3]
except:
	sys.exit(1)

try:
	_QUESTIONS_PATH  = sys.argv[4]
except:
	_QUESTIONS_PATH = None

_FILE_HR = open(_FILE_PATH,'r')

_hrValues= []
for _hrRegistry in _FILE_HR:
	_lines = _hrRegistry.split(",")
	if (_lines[2] == "heart_rate"):
		_value =  float( _lines[3].replace("\n","") )
		_hrValues.append(_value)
_QUESTIONS_START_TIMES = []
_QUESTIONS_END_TIMES = []
if( _QUESTIONS_PATH != None):
	_QUESTIONS_FILE = open(_QUESTIONS_PATH,"r")
	for _line in _QUESTIONS_FILE:
		if "START" in _line:
			_value = int (_line.split(",")[1] )
			_QUESTIONS_START_TIMES.append( _value)
		if "END" in _line:
			_value = int (_line.split(",")[1] )
			_QUESTIONS_END_TIMES.append( _value)
			
import pylab as plt
import numpy as np
#init the plot
fig, ax = plt.subplots()
index = np.arange( len(_hrValues))
bar_width = 1


ax.plot(_hrValues,color='red')
#plot questions
leyendDisplayed = False
if(_QUESTIONS_PATH != None):
	for _question in _QUESTIONS_START_TIMES:
		_startPlot, = ax.plot(_question,_hrValues[_question],".",color='green')
	for _question in _QUESTIONS_END_TIMES:
		_endPlot, = ax.plot(_question,_hrValues[_question],".",color='blue')
	if not ( leyendDisplayed):
		from matplotlib.pyplot import *
		l1 = ax.legend([_startPlot], ["Question Starts"], loc=3)
		l2 = ax.legend([_endPlot], ["Question Ends"], loc=4)
		gca().add_artist(l1)
		leyendDisplayed = True
#set the labels
ax.set_ylabel('HR Value')
ax.set_xlabel('Time (Seconds)' )
ax.set_title('HR Value from:[%s]' % _SUBJECT_NAME)
ax.grid(True)
plt.ylim([55,95])
#show it
plt.tight_layout()
plt.savefig(_OUTPUT_FIG_PATH)
#plt.show()

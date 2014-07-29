import sys
def isBlink(points):
	_threshold = _THRESHOLD
	_avg = ( points[0] + points[1] + points[2] +points[6] +points[7] + points[8]  ) / 6
	if ( points[4] - _avg  < _threshold ): 
		return False
	else:
		return True
try:
	_FILE_PATH =  sys.argv[1]
	_SUBJECT_NAME = sys.argv[2]
	_STEP = int (sys.argv[3] )
	_THRESHOLD = float ( sys.argv[4] )
except:
	sys.exit(1)
	
_file = open(_FILE_PATH,'r')
_data = []
_dates = []
for _line in _file:
	_l = _line.replace("\n","")
	_splits = _l.split(",")
	if  (_splits[2].strip(" ")  !="blink" ) :
		_data.append( float ( _splits[2]) ) 
		_dates.append(_splits[0])

_sec = 26

#_data2 = _data[40000:40000 + (_sec *10)]
import pylab as plt
import numpy as np
#init the plot
fig, ax = plt.subplots()
index = np.arange( len(_data))
bar_width = 1

#move window
#calculate max number of windows
_maxWindows = int ( len ( _data ) / 9) 
print "Dataset Lenght: %s" % str( len( _data))
print "Max windows: %s" % str( _maxWindows)
_Blinks = []
_BlinkDates = []
_step = _STEP
for _w in range(0, ( (_maxWindows-1)   * 9 ) ,_step):
	if (isBlink(_data[_w:_w+9])):
		_Blinks.append(_data[_w+4])
		_BlinkDates.append(_w+4)

print "Blinks: %s" % str( len(_Blinks) )
_w= 0 
for _blink in _Blinks:
	print _blink
	plt.plot(_BlinkDates[_w],_blink,'go')
	_w +=1
#calculate blink
plt.plot(_data)
#draw lines
#plt.plot([25,25])

#plt.axhline(y=0, xmin=0, xmax=1)

#set the width
#plt.xticks(index +.5 , _ACTIVITY_DATES,rotation=90)
#set the labels
ax.set_ylabel('IR Value')
ax.set_xlabel('Time')
ax.set_title('IR Value from:[%s]' % _SUBJECT_NAME)
ax.grid(True)
#show it
plt.tight_layout()
plt.show()


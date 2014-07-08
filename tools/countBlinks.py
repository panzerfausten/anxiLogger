import sys

def usage():
	print "USAGE:"
	print "		python countBlinks <FILE>"
try:
	_INPUTURL  = sys.argv[1]
except:
	usage()
	sys.exit(1)

try:
	_FILE = open(_INPUTURL,"r")
except:
	print "Error reading file"
	sys.exit(1)

_blinkCounts = 0	
for _line in _FILE:
	if "blink" in _line:
		_blinkCounts  += 1
print "Total blinks: %i" % _blinkCounts

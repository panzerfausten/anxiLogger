import sys

try:
        _FILE_PATH = sys.argv[1]
except:
        sys.exit(1)

_FILE_HR = open(_FILE_PATH,'r')

_hrValues= []
_totalHR =  0
for _hrRegistry in _FILE_HR:
        _lines = _hrRegistry.split(",")
        if (_lines[2] == "heart_rate"):
                _value =  float( _lines[3].replace("\n","") )
                _hrValues.append(_value)
		_totalHR = _totalHR + _value
print _totalHR/ len (_hrValues)

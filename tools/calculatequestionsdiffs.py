import sys
try:
	_HR_INPUT  = sys.argv[1]
	_BLINKS_INPUT  = sys.argv[2]
	_QUESTIONS_INPUT  = sys.argv[3]
	_SUBJECT  = sys.argv[4]
except:
	print "USAGE: python calculatequestionsdiffs.py HRINPUTFILE BLINKSINPUTFILE QUESTIONSINPUTFILE"
	sys.exit(1)
_HR_FILE = open(_HR_INPUT,"r")
_BLINKS_FILE = open(_BLINKS_INPUT,"r")
_QUESTIONS_FILE = open(_QUESTIONS_INPUT,"r")

_HR_VALUES= []
for _hrRegistry in _HR_FILE:
        _lines = _hrRegistry.split(",")
        if (_lines[2] == "heart_rate"):
                _value =  float( _lines[3].replace("\n","") )
                _HR_VALUES.append(_value)

_QUESTIONS_START_TIMES = []
_QUESTIONS_END_TIMES = []
for _line in _QUESTIONS_FILE:
	if "START" in _line:
		_value = int (_line.split(",")[1] )
		_QUESTIONS_START_TIMES.append( _value)
	if "END" in _line:
		_value = int (_line.split(",")[1] )
		_QUESTIONS_END_TIMES.append( _value)
_BLINKS_DATA = []
for _BLINK in _BLINKS_FILE:
	_BLINKS_DATA.append(_BLINK)

_BLINKS_COUNT_PER_SECOND = [0] * len (_HR_VALUES)
for i,_BLINK in enumerate(_BLINKS_DATA):
	try:
		count = int (_BLINK)
	except:
		print "FILE: %s ERROR LINE:%i %s" % ( _BLINKS_INPUT,i, _BLINK)
	_BLINKS_COUNT_PER_SECOND[count] = _BLINKS_COUNT_PER_SECOND[count] + 1
#print "Input size: HR:[%i] BLINKS[%i] QUESTIONS[%i]" % ( len(_HR_VALUES),len(_BLINKS_DATA), len(_QUESTIONS_START_TIMES))
#print "QUESTION #,AVG_HR_BEFORE_QUESTION,AVG_HR_AFTER_QUESTION,DIFF_HR,AVG_SBR_BEFORE_QUESTION,DIFF_SBR"
for counter,_q in enumerate(_QUESTIONS_START_TIMES):
	c= counter +1 
	_avg_hr_before_question = sum ( _HR_VALUES[_q-15:_q] ) / 15.0
	_avg_hr_after_question = sum ( _HR_VALUES[_q:_q+15] ) / 15.0
	_diff_hr = _avg_hr_after_question - _avg_hr_before_question
	_avg_sbr_before_question = sum ( _BLINKS_COUNT_PER_SECOND[_q-15:_q] ) / 15.0
	_avg_sbr_after_question = sum ( _BLINKS_COUNT_PER_SECOND[_q:_q+15] ) / 15.0
	_diff_sbr = _avg_sbr_after_question - _avg_sbr_before_question
	print "%s,QUESTION %i,%f,%f,%f,%f,%f,%f" % (_SUBJECT,c,_avg_hr_before_question , _avg_hr_after_question, _diff_hr, _avg_sbr_before_question , _avg_sbr_after_question, _diff_sbr)
	


anxiLogger
==========

A python application to gather data from zephyrHxM and Google glass data 

Includes Zephyr-bt library

https://github.com/jpaalasm/zephyr-bt

USAGE 
==========
		USAGE: python read_from_device.py [OPTIONS] [outputfile]
			OPTIONS:
			--nolog: avoids saving to disk
			--sample: Takes a sample of 5 minutes of data
		EXAMPLE:
			Running in sample mode
			python anxiLogger.py --sample logs/subject
			
			Running in ANXIETY INDUCTION  mode
			python anxiLogger.py logs/subject


Darien Miranda <dmiranda@cicese.edu.mx>

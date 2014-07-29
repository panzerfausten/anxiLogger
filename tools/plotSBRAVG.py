import sys

try:
	_FILE_PATH = sys.argv[1]
	_SUBJECT_NAME = sys.argv[2]
	_FIG_OUT_PATH = sys.argv[3]
except:
	sys.exit(1)

_FILE_SBR = open(_FILE_PATH,'r')

_sbrValues= []
for _sbrValue in _FILE_SBR:
	_sbrValues.append(_sbrValue)

import pylab as plt
import numpy as np
#init the plot
fig, ax = plt.subplots()
index = np.arange( len(_sbrValues))
bar_width = 1


ax.plot(_sbrValues)
#set the labels
ax.set_ylabel('SBR Value')
ax.set_xlabel('Time (minutes)')
ax.set_title('AVG SBR Values from:[%s]' % _SUBJECT_NAME)
ax.grid(True)
plt.ylim([10,80])
#show it
plt.tight_layout()
plt.savefig(_FIG_OUT_PATH)
#plt.show()

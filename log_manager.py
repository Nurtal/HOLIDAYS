"""
Log management function
"""

import os
import glob
import datetime

def init_logs():
	"""
	-> Clean the log folder
	-> create an empty log file
	"""

	## clean folder
	files_to_remove = glob.glob("log/*")
	for f in files_to_remove:
		os.remove(f)

	## get time
	now = datetime.datetime.now()
	date = str(now.day)+"_"+str(now.month)+"_"+str(now.year)

	## create new log file
	log_file_name = "log/"+date+".log"
	log_file = open(log_file_name, "w")
	log_file.close()


def get_current_log_file():
	"""
	-> return the current log file (i.e log file of the day)
	-> create one if it does not exist
	"""

	## get the name of the current log file
	now = datetime.datetime.now()
	date = str(now.day)+"_"+str(now.month)+"_"+str(now.year)
	log_file_name = "log/"+date+".log"

	## create new log file if it does not already exist
	if(not os.path.exists(log_file_name)):
		log_file = open(log_file_name, "w")
		log_file.close()

	return log_file_name



def add_entry(entry):
	"""
	-> add a line to the current log_file
	"""

	## get time
	now = datetime.datetime.now()
	date = date = "["+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+"|"+str(now.day)+"/"+str(now.month)+"]"

	## get current log file
	log_file_name = get_current_log_file()

	## Prepare the entry
	line_to_write = date+str(entry)+"\n"

	## write the entry
	log_file = open(log_file_name, "a")
	log_file.write(line_to_write)
	log_file.close()

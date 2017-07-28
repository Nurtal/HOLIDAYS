"""
Log management function
"""

import os
import glob
import datetime
import platform

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import requests
from lxml import html

from email.MIMEBase import MIMEBase
from email import encoders

import random
import os.path
from time import sleep

def init_logs():
	"""
	-> Clean the log folder
	-> create an empty log file
	-> create the log manifeste file
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

	## create the manifeste log file
	manifeste_file = open("log/log_send.csv", "w")
	manifeste_file.close()


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


def send_log_file(log_file):
	"""
	-> Send log files by email
	-> TODO:
		- Update the message, add randomness, be nice
		- Don'y forget to set passwd variable !
	"""

	fromaddr = "nathan.foulquier@cervval.com"
	toaddr = "nathan.foulquier.pro@gmail.com"
	passwd = FIXEME

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "update from the office"
 
	body = "Hey Boss, update from work"
 
	msg.attach(MIMEText(body, 'plain'))
 
 	filename = "undef"
 	if(platform.system() == "Windows"):
		filename = log_file.split("\\")
		filename = filename[-1]
	elif(platform.system() == "Linux"):
		filename = log_file.split("/")
		filename = filename[-1]

	attachment = open(log_file, "rb")
 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
	msg.attach(part)
 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, passwd)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


def monitoring_log():
	"""
	-> Check if there is an old log file to send
	-> Send the log file by email
	-> update the log manifeste file
	"""

	## get time
	now = datetime.datetime.now()
	date = str(now.day)+"_"+str(now.month)+"_"+str(now.year)
	log_file_name = "log/"+date+".log"

	## get list of log already send
	log_already_sends = []
	manifeste_file = open("log/log_send.csv", "r")
	for line in manifeste_file:
		line = line.replace("\n", "")
		log_already_sends.append(line)
	manifeste_file.close()

	## get available log
	list_of_log_files = glob.glob("log/*.log")
	
	## Get the list of old logs
	old_logs = []
	for f in list_of_log_files:
		if(f != log_file_name and f not in log_already_sends):
			old_logs.append(f)

	for f in old_logs:
		send_log_file(f)

		manifeste_file = open("log/log_send.csv", "a")
		manifeste_file.write(f+"\n")
		manifeste_file.close()

"""
Log management function
"""

import os
import glob
import datetime
import platform
import psutil

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


passwd = FIXEME


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




def get_a_nice_message(log_file):
	"""
	-> Parse log file, scan available disk space
	   and create a nice message for the update email
	"""

	possible_salutation = ["Hey Boss!",
						   "Still up and Running !",
						   "Still working",
						   "Keeping the CPU busy !",
						   "Another great day for Science ...",
						   "Lok'tar Ogar",
						   "Bal'a dash, malanore"]

	salutation = possible_salutation[random.randint(0,len(possible_salutation)-1)]

	## get the name of work station
	station_name = ""
	if(platform.system() == "Windows"):
		station_name = "Morvan"
	elif(platform.system() == "Linux"):
		station_name = "Cervval"
	station_id = "Report from "+str(station_name)+":\n"


	## Get informations on log file
	server_id = []
	analysis_performed = 0
	analysis_skipped = 0
	log_file = open(log_file, "r")
	for line in log_file:
		line = line.replace("\n", "")

		## count the number of analysis performed
		line_in_array = line.split("[+] Run analysis")
		if (len(line_in_array) > 1):
			analysis_performed += 1

		## count the number of case skipped:
		line_in_array = line.split("Skip case")
		if (len(line_in_array) > 1):
			analysis_skipped += 1

		## check server status
		line_in_array = line.split("server ")
		if (len(line_in_array) > 1):
			server_id.append(line_in_array[1])
	
	log_file.close()
	
	## message for server status
	if(len(server_id) > 0):
		last_server_id = server_id[-1]
		server_news = ""
		if(last_server_id == "1"):
			server_news = "Server 1 Up and Running."
		elif(last_server_id == "2"):
			server_news = "Server 1 is down, Server 2 Up and Running." 
	else:
		server_news = "Server 1 and Server 2 are down."

	
	## information on hard drive capacity
	free_space = psutil.disk_usage(".").free
	free_space = free_space / 1024 #ko
	free_space = free_space / 1024 #Mo
	free_space = free_space / 1024 #Go
	disk_news = "Space available on disk: " +str(free_space) +" Go."


	## Create message
	text = str(analysis_performed) +" analysis were performed yesterday, "+str(analysis_skipped)+" were skipped.\n"
	text += "Server status for yesterday: "+str(server_news)+"\n"
	text += disk_news
	if(analysis_skipped < 10):
		text += "\nI am keeping this cpu busy !"
	elif(analysis_performed < 10):
		text += "\nYeah ... a lot of NA ..."

	## assemble message
	final_message = salutation+"\n"+station_id+text

	return final_message


def send_log_file(log_file):
	"""
	-> Send log files by email
	-> TODO:
		- Don't forget to set passwd variable !
	"""

	fromaddr = "nathan.foulquier@cervval.com"
	toaddr = "nathan.foulquier.pro@gmail.com"
	#passwd = FIXEME

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


def send_end_message():
	"""
	-> Send an email when hit the end of the programm
	"""

	fromaddr = "nathan.foulquier@cervval.com"
	toaddr = "nathan.foulquier.pro@gmail.com"
	#passwd = FIXEME

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "EOF"
 
	## get the name of work station
	station_name = ""
	if(platform.system() == "Windows"):
		station_name = "Morvan"
	elif(platform.system() == "Linux"):
		station_name = "Cervval"

	content = "Hey Boss,\n"+str(station_name)+": Work done."

	msg.attach(MIMEText(content, 'plain'))
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, passwd)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
"""
Function for the holidays
Project
"""

import itertools
import glob
import os

def build_data_file_from(explain_variable, descriptives_variable, data_file, output_name):
	"""
	-> Build a new file from data_file
	-> explain_variable is a string, the name of the variable to explain (the first column)
	-> descriptives_variable is a list of descriptives_variable
	"""

	index_to_variable = {}
	variable_to_index = {}
	index_to_variable_in_new_array = {}

	data = open(data_file, "r")
	output = open(output_name, "w")
	cmpt = 0

	## Prepare header
	header = ""
	header += explain_variable+","
	index_to_variable_in_new_array[0] = explain_variable
	index = 1
	for var in descriptives_variable:
		header += var +","
		index_to_variable_in_new_array[index] = var
		index +=1
	header = header[:-1]
	output.write(header+"\n")
	for line in data:
		line = line.replace("\n", "")
		line_in_array = line.split(",")
		if(cmpt == 0):
			index = 0
			for var in line_in_array:
				if(explain_variable == var):
					index_to_variable[explain_variable] = index
					variable_to_index[var] = index
				elif(var in descriptives_variable):
					index_to_variable[var] = index
					variable_to_index[var] = index
				index += 1
		else:
			line_to_write = ""
			line_to_write += line_in_array[variable_to_index[explain_variable]]+","
			for var in descriptives_variable:
				line_to_write += line_in_array[variable_to_index[var]] + ","
			line_to_write = line_to_write[:-1]
			output.write(line_to_write+"\n")
		cmpt +=1
	output.close()
	data.close()


def drop_patients_with_NA(input_file):
	"""
	-> Create a new file from input_file and
	   drop every line containing NA values
	"""

	data_file_name = input_file.split(".")
	data_file_name = data_file_name[0]
	output_name = str(data_file_name)+"_without_NA.csv"

	input_data = open(input_file, "r")
	output_data = open(output_name, "w")

	for line in input_data:
		line = line.replace("\n", "")
		line_in_array = line.split(",")

		keep_the_line = True

		if("NA" in line_in_array):
			keep_the_line = False

		if(keep_the_line):
			output_data.write(line+"\n")

	output_data.close()
	input_data.close()


def control_subset_file(file_to_test):
	"""
	-> count the number of line in a file
	-> return True if > 10 cases in file, if not return False
	"""

	data = open(file_to_test, "r")
	cmpt = 0
	for line in data:
		cmpt += 1
	data.close()
	enought_patient_in_file = True
	if(cmpt < 10):
		enought_patient_in_file = False

	return enought_patient_in_file



def get_description_of_variables(input_file):
	"""
	-> Try to figure out if variables describe in input_file are
	   qualitative or quantitative.
	-> return a dict with the name of quantitative and qualitative variable
	"""
	type_to_variables = {}
	type_to_variables["qualitative"] = []
	type_to_variables["quantitative"] = []

	## Get the data 
	index_to_variable = {}
	variable_to_value = {}
	input_data = open(input_file, "r")
	cmpt = 0
	for line in input_data:
		line = line.replace("\n", "")
		line_in_array = line.split(",")
		if(cmpt == 0):
			index = 0
			for var in line_in_array:
				index_to_variable[index] = var
				variable_to_value[var] = []
				index += 1
		else:
			index = 0
			for scalar in line_in_array:
				variable_to_value[index_to_variable[index]].append(scalar)
				index += 1
		cmpt += 1
	input_data.close()

	## Test if variable is qualitative or not
	quantitative_variable = []
	qualitative_variable = []
	for key in variable_to_value.keys():
		var_is_quantitative = True
		for scalar in variable_to_value[key]:
			if(scalar != "NA"):
				try:
					scalar = float(scalar)
				except:
					var_is_quantitative = False
		if(var_is_quantitative):
			quantitative_variable.append(key)
		else:
			qualitative_variable.append(key)
	type_to_variables["qualitative"] = qualitative_variable
	type_to_variables["quantitative"] = quantitative_variable

	## return the results
	return type_to_variables




def generate_all_possible_combinations(explain_variables, descriptives_variables):
	"""
	-> generate all possibles combination of descriptives variables
	   to explain each variables in explain_variables
	-> explain_variables and descriptives_variables are list obtained with the get_description_of_variables function
	-> write the combinations (associated with an id) in the input/suggestions.csv file
	"""

	manifeste_file = open("data/suggestions.csv", "w")
	cmpt = 0
	for exp_var in explain_variables:
		header = []
		header.append(exp_var)
		tupleLen = 4
		while(tupleLen <= len(descriptives_variables)):
			for h in itertools.combinations(descriptives_variables, tupleLen):
				h = list(h)
				h = header + h
				line_to_write = ""
				for elt in h:
					line_to_write += str(elt)+","
				line_to_write  =str(cmpt) +","+ line_to_write[:-1]
				manifeste_file.write(line_to_write+"\n")
				cmpt += 1
			tupleLen += 1
	manifeste_file.close()



def clean_data_folder():
	"""
	-> clean all files present in input folder
	"""
	files_to_remove = glob.glob("data/*")
	for f in files_to_remove:
		os.remove(f)



def clean_reports_folder():
	"""
	-> clean all tex and pdf files present in reports folder
	"""
	files_to_remove = glob.glob("output/reports/*.pdf")
	for f in files_to_remove:
		os.remove(f)

	files_to_remove = glob.glob("output/reports/*.tex")
	for f in files_to_remove:
		os.remove(f)


def clean_images_folder():
	"""
	-> clean all png files present in reports folder
	"""
	files_to_remove = glob.glob("output/images/*.png")
	for f in files_to_remove:
		os.remove(f)











## TEST SPACE
#variables = get_description_of_variables("input/input_test.csv")
#generate_all_possible_combinations(variables["qualitative"], variables["quantitative"])


import urllib
import requests

def uploadfile(filepath, uploadurl, fileformelementname="upfile"):
    '''
    This will invoke an upload to the webserver
    on the VM
    '''
 
    files = {fileformelementname : open(filepath,'rb')}
    r = requests.post(uploadurl, files=files)
    return r.status_code



def downloadfile(filename, dloadurl, outputdirectory):
    '''
    Pull the converted file off the droopy server
    '''
 
    fullurl = urljoin(dloadurl, filename)
    fulloutputpath = os.path.join(outputdirectory, 'divided', filename)
 
    urllib.urlretrieve(fullurl, fulloutputpath)



#downloadfile(currentFile.outputName, DOWNLOADURL, IMGDIR)
#uploadStatus = uploadfile("C:/Users/Doctorant/Desktop/Nathan/Spellcraft/HOLIDAYS/up_test.txt", "http://195.83.246.52:8000", "upfile")

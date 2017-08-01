"""
ANALYSIS STUFF
"""

import os
import shutil

def run_afd(input_data):
	"""
	IN PROGRESS
	"""

	## Prepare the file for R script
	if(input_data != "data/data.csv"):
		shutil.copy(input_data, "data/data.csv")

	## Run the R script
	os.system("Rscript scripts/afd_script.R > trash.txt")



def prepare_afd_script():
	"""
	-> Get the variable to explain (left element of the formula in R)
	   from the data file (assume its always the first column)
	-> Write a R script for the variable to explain
	-> Warning!, work only of the afd_template script is left unchanged !
	"""

	## get the variable to explain
	var_to_explain = "undef"
	cmpt = 0
	data_file = open("data/data.csv", "r")
	for line in data_file:
		if(cmpt == 0):
			line_in_array = line.split(",")
			var_to_explain = line_in_array[0]
		cmpt += 1
	data_file.close()
	var_to_explain = var_to_explain.replace("\\", ".")
	if(var_to_explain[0] == "."):
		var_to_explain = "X" + var_to_explain

	## write the script
	template_file = open("scripts/afd_template.R", "r")
	afd_script = open("scripts/afd_script.R", "w")
	cmpt = 1
	for line in template_file:
		if(cmpt == 108):
			line_to_write = "data.lda <- lda("+str(var_to_explain)+" ~ ., data=data)"
			afd_script.write(line_to_write+"\n")
		elif(cmpt == 123):
			  line_to_write = "ldahist(data = data.lda.values$x[,comp], g="+str(var_to_explain)+")"
			  afd_script.write(line_to_write+"\n")
		elif(cmpt == 132):
			line_to_write = "text(data.lda.values$x[,1],data.lda.values$x[,2],"+str(var_to_explain)+",cex=0.7,pos=4,col=\"red\")"
			afd_script.write(line_to_write+"\n")
		else:
			afd_script.write(line)
		cmpt += 1
	afd_script.close()
	template_file.close()
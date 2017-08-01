"""
main holdays
"""

import shutil
import os

import analysis
import report
import file_manager
import log_manager
import holidays


#input_data_file = "input/input_test2.csv"
input_data_file = "input/transmart.txt"
work_station = "cervval"

##-----------------------------##
## Preprocessing the data file ##
##-----------------------------##
log_manager.init_logs()
holidays.clean_data_folder()
holidays.clean_reports_folder()
input_data_file = file_manager.fix_file_name(input_data_file)
file_manager.change_file_format(input_data_file, ",")
original_extention = input_data_file.split(".")
original_extention = original_extention[-1]
input_data_file = input_data_file.replace("."+str(original_extention), "_reformated.csv")
shutil.copy(input_data_file, "data/complete_data.csv")


##------------------##
## Run the analysis ##
##------------------##
variables = holidays.get_description_of_variables("data/complete_data.csv")
holidays.generate_all_possible_combinations(variables["qualitative"], variables["quantitative"], 10)

suggestions_file = open("data/suggestions.csv", "r")
for line in suggestions_file:
	line = line.replace("\n", "")
	line_in_array = line.split(",")
	
	## Get composition of the suggestion
	suggestion_id = line_in_array[0]
	variable_to_explain = line_in_array[1]
	descriptives_variables = line_in_array[2:]

	## Build the suggestion
	holidays.build_data_file_from(variable_to_explain, descriptives_variables, "data/complete_data.csv", "data/data.csv")

	## Drop NA
	holidays.drop_patients_with_NA("data/data.csv")
	shutil.copy("data/data_without_NA.csv", "data/data.csv")

	## Test if file still contains enough cases
	valid_file_for_analysis = holidays.control_subset_file("data/data.csv")

	## Perform the analysis
	if(valid_file_for_analysis):

		## Clean the images folder
		holidays.clean_images_folder()

		## Log entry
		log_manager.add_entry("[+] Run analysis for case "+str(suggestion_id))

		## Prepare the R script
		analysis.prepare_afd_script()

		## Run the LDA analysis
		analysis.run_afd("data/data.csv")

		## Write a report on the analysis
		report.write_lda_report("output/reports/LDA_report_case_"+str(suggestion_id)+".tex")

		## Compile report
		report.compile_report("output/reports/LDA_report_case_"+str(suggestion_id)+".tex")

		## Save to other computers
		report_have_been_saved = False
		absolute_path_to_file = os.path.abspath("output/reports/LDA_report_case_"+str(suggestion_id)+".pdf")

		if(work_station != "cervval"):

			## Try the first server
			uploadStatus = holidays.uploadfile(absolute_path_to_file, "http://195.83.246.52:8000", "upfile")
			if(uploadStatus == 200):
				log_manager.add_entry("[+] Saved report for case "+str(suggestion_id)+" on server 1")
				report_have_been_saved = True

			## Try the second server if the first failed
			else:
				uploadStatus = holidays.uploadfile(absolute_path_to_file, "http://195.83.246.20:8000", "upfile")
				if(uploadStatus == 200):
					log_manager.add_entry("[+] Saved report for case "+str(suggestion_id)+" on server 2")
					report_have_been_saved = True

		## Delete report from local storage if it has been saved elsewhere
		if(report_have_been_saved):
			os.remove(absolute_path_to_file)
		else:
			log_manager.add_entry("[!] Fail to save report for case "+str(suggestion_id)+" on a distant server")

	else:
		## Log entry
		log_manager.add_entry("[-] Skip case "+str(suggestion_id) +", not enough patients in file")


	## Check on log
	log_manager.monitoring_log()

suggestions_file.close()

## Add end Message
log_manager.add_entry("[*] End of Run\n")
log_manager.send_end_message()


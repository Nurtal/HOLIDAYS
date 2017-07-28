"""
main holdays
"""

import shutil

import analysis
import report
import file_manager
import log_manager
import holidays


input_data_file = "input/input_test2.csv"

##-----------------------------##
## Preprocessing the data file ##
##-----------------------------##
log_manager.init_logs()
holidays.clean_data_folder()
holidays.clean_reports_folder()
input_data_file = file_manager.fix_file_name(input_data_file)
file_manager.change_file_format(input_data_file, ",")
input_data_file = input_data_file.replace(".csv", "_reformated.csv")
shutil.copy(input_data_file, "data/complete_data.csv")


##------------------##
## Run the analysis ##
##------------------##
variables = holidays.get_description_of_variables("data/complete_data.csv")
holidays.generate_all_possible_combinations(variables["qualitative"], variables["quantitative"])

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

		## Run the LDA analysis
		analysis.run_afd("data/data.csv")

		## Write a report on the analysis
		report.write_lda_report("output/reports/LDA_report_case_"+str(suggestion_id)+".tex")

		## Compile report
		report.compile_report("output/reports/LDA_report_case_"+str(suggestion_id)+".tex")
	else:
		## Log entry
		log_manager.add_entry("[-] Skip case "+str(suggestion_id) +", not enough patients in file")

	## Check on log
	log_manager.monitoring_log()



suggestions_file.close()



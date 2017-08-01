"""
REPORTING TOOLS
"""

import datetime
import glob
import platform
import os
import shutil

def write_lda_report(report_file):
	"""
	-> Write a 3 section reports for the LDA analysis
	-> section 1 is an overview of the data
	-> section 2 privide informations on the LDA
	-> section 3 is a 2D representation of the data using LDA

	- TODO:
		- Find a way to get absolute path on windows for the image files,
		  for now path is store as a prefix directly in the code

	IN PROGRESS
	"""

	now = datetime.datetime.now()


	title = "LDA Automatic report"
	date = str(now.day)+"/"+str(now.month)+"/"+str(now.year)

	##************##
	## Write file ##
	##************##
	output_file = open(report_file, "w")

	## Write header
	output_file.write("\\documentclass[a4paper,9pt]{extarticle}\n\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n\\usepackage{graphicx}\n\\usepackage{xcolor}\n\\usepackage{tikz}\n\\usepackage{pgfplots}\n\\usepackage{amsmath,amssymb,textcomp}\n\\everymath{\\displaystyle}\n\n\\usepackage{times}\n\\renewcommand\\familydefault{\\sfdefault}\n\\usepackage{tgheros}\n\\usepackage[defaultmono,scale=0.85]{droidmono}\n\n\\usepackage{multicol}\n\\setlength{\\columnseprule}{0pt}\n\\setlength{\\columnsep}{20.0pt}\n\n\n\\usepackage{geometry}\n\\geometry{\na4paper,\ntotal={210mm,297mm},\nleft=10mm,right=10mm,top=10mm,bottom=15mm}\n\n\\linespread{1.3}\n\n\n% custom title\n\\makeatletter\n\\renewcommand*{\\maketitle}{%\n\\noindent\n\\begin{minipage}{0.4\\textwidth}\n\\begin{tikzpicture}\n\\node[rectangle,rounded corners=6pt,inner sep=10pt,fill=blue!50!black,text width= 0.75\\textwidth] {\\color{white}\\Huge \\@title};\n\\end{tikzpicture}\n\\end{minipage}\n\\hfill\n\\begin{minipage}{0.55\\textwidth}\n\\begin{tikzpicture}\n\\node[rectangle,rounded corners=3pt,inner sep=10pt,draw=blue!50!black,text width= 0.95\\textwidth] {\\LARGE \\@author};\n\\end{tikzpicture}\n\\end{minipage}\n\\bigskip\\bigskip\n}%\n\\makeatother\n\n% custom section\n\\usepackage[explicit]{titlesec}\n\\newcommand*\sectionlabel{}\n\\titleformat{\\section}\n{\\gdef\\sectionlabel{}\n\\normalfont\\sffamily\\Large\\bfseries\\scshape}\n{\\gdef\\sectionlabel{\\thesection\ }}{0pt}\n{\n\\noindent\n\\begin{tikzpicture}\n\\node[rectangle,rounded corners=3pt,inner sep=4pt,fill=blue!50!black,text width= 0.95\\columnwidth] {\\color{white}\\sectionlabel#1};\n\\end{tikzpicture}\n}\n\\titlespacing*{\\section}{0pt}{15pt}{10pt}\n\n\n% custom footer\n\\usepackage{fancyhdr}\n\\makeatletter\n\\pagestyle{fancy}\n\\fancyhead{}\n\\fancyfoot[C]{\\footnotesize \\textcopyright\\ \\@date\\ \\ \\@author}\n\\renewcommand{\\headrulewidth}{0pt}\n\\renewcommand{\\footrulewidth}{0pt}\n\\makeatother\n\n\n\\title{"+str(title)+"}\n\\author{FIXEME}\n\\date{"+str(date)+"}\n")
	output_file.write("\\begin{document}\n\\maketitle\n")


	##------------------------##
	## Write overview section ##
	##------------------------##
	## -> TODO: Adapt to the number of figures
	
	output_file.write("\\section{Overview}\n")
	output_file.write("\\begin{center}\n")
	output_file.write("\\begin{tabular}{c}\n")

	## => Create a tabular for image in report
	list_of_scatterplot = glob.glob("output/images/scatterplot_*")
	output_file.write("\\begin{tabular}{c}\n")
	for image in list_of_scatterplot:
		image = image.split(".")
		image = image[0]
		if(platform.system() == "Windows"):
			image = image.replace("\\", "/")
			prefix = "C:/Users/PC_immuno/Desktop/Nathan/SpellCraft/HOLIDAYS/"
			image = prefix + image
		if(os.path.exists(image)):
			output_file.write("\\includegraphics[scale=0.5]{\""+str(image)+"\"}\\\\ \n")
		else:
			output_file.write("Image not found\\\\ \n")
	output_file.write("\\end{tabular}\n")

	## => Write some informations from files
	## Get the number of line to generate (i.e the number of category)
	## Get the number of items by category
	category_to_number = {}
	number_of_category = 0
	lda_count_file = open("output/lda_count_file.csv", "r")
	for line in lda_count_file:
		line = line.replace("\n", "")
		if(line != "\"x\""):
			number_of_category += 1
			line_in_array = line.split(",")
			category_to_number[line_in_array[0]] = line_in_array[1]
	lda_count_file.close()

	## Get the proportion of category
	category_to_proportion = {}
	lda_prior_file = open("output/lda_prior_file.csv", "r")
	for line in lda_prior_file:
		line = line.replace("\n", "")
		if(line != "\"x\""):
			line_in_array = line.split(",")
			category_to_proportion[line_in_array[0]] = line_in_array[1]
	lda_prior_file.close()

	## Get total count of items
	total_count = 0
	for value in category_to_number.values():
		total_count += int(value)



	## Write the table
	output_file.write("\\\\ \n")
	output_file.write("\\begin{tabular}{|c|c|c|}\n")
	output_file.write("\\hline\n")
	output_file.write("Category & Number & proportion \\\\ \n")
	output_file.write("\\hline\n")
	for key in category_to_number.keys():
		tabular_line = key + " & " +str(category_to_number[key]) + " & " + str(category_to_proportion[key]) + " \\\\ \n"
		output_file.write(tabular_line)
		output_file.write("\\hline\n")
	output_file.write("Total & "+str(total_count)+" & 1 \\\\ \n")
	output_file.write("\\hline\n")
	output_file.write("\\end{tabular}\n")
	output_file.write("\\end{tabular}\n")


	## [IN PROGRESS: Adapt to the number of figures]
	"""
	if(len(list_of_scatterplot) == 1):
		output_file.write("\\begin{tabular}{c}\n")
		output_file.write("\\includegraphics[scale=0.5]{\""+str(list_of_scatterplot[0])+"\"}")
		output_file.write("\\end{tabular}\n")
	"""
	output_file.write("\\end{center}\n")


	##----------------------------##
	## Write LDA analysis section ##
	##----------------------------##

	## => Plot the figures
	## TODO: Adapt to the number of figures
	output_file.write("\\section{LDA description}\n")
	output_file.write("\\begin{center}\n")
	output_file.write("\\begin{tabular}{c}\n")


	list_of_LDA = glob.glob("output/images/*_histogram.png")
	output_file.write("\\begin{tabular}{c}\n")
	for image in list_of_LDA:
		image = image.split(".")
		image = image[0]
		if(platform.system() == "Windows"):
			image = image.replace("\\", "/")
			prefix = "C:/Users/PC_immuno/Desktop/Nathan/SpellCraft/HOLIDAYS/"
			image = prefix + image
		if(os.path.exists(image)):
			output_file.write("\\includegraphics[scale=0.5]{\""+str(image)+"\"}\\\\ \n")
		else:
			output_file.write("Image not found\\\\ \n")
	output_file.write("\\end{tabular}\n")

	output_file.write("\\\\ \n")

	## => Get informations about the LDA
	lda_to_var_to_value = {}
	index_to_lda = {}
	scaling_file = open("output/lda_scaling_file.csv", "r")
	cmpt_line = 0
	for line in scaling_file:
		line = line.replace("\n", "")
		line_in_array = line.split(",")
		if(cmpt_line == 0):
			index = 0
			for element in line_in_array:
				lda_to_var_to_value[element] = {}
				index_to_lda[index] = element
				index += 1
		else:
			index = 0
			var = line_in_array[0]
			for element in line_in_array[1:]:
				lda_to_var_to_value[index_to_lda[index]][var] = element
				index += 1
		cmpt_line += 1
	scaling_file.close()

	## => Write informations about the LDA
	col_disposition = "|c|"
	first_line = "&"
	for element in lda_to_var_to_value.keys():
		col_disposition += "c|"
		first_line += str(element) +"&"
	first_line = first_line[:-1] + "\\\\ \n"
	output_file.write("\\begin{tabular}{"+str(col_disposition)+"}\n")
	output_file.write("\\hline\n")
	output_file.write(first_line)
	output_file.write("\\hline\n")
	list_of_variables = []
	for var in lda_to_var_to_value.values():
		for element in var.keys():
			if(element not in list_of_variables):
				list_of_variables.append(element)
	for var in list_of_variables:
		line_to_write = str(var) + "&"
		for key in lda_to_var_to_value.keys():
			line_to_write += str(lda_to_var_to_value[key][var]) +"&"
		line_to_write = line_to_write[:-1] +" \\\\ \n"
		output_file.write(line_to_write)
		output_file.write("\\hline\n")
	output_file.write("\\end{tabular}\n")
	output_file.write("\\end{tabular}\n")
	output_file.write("\\end{center}\n")

	##------------------------------##
	## Write Representation section ##
	##------------------------------##

	output_file.write("\\section{2D representation}\n")
	output_file.write("\\begin{center}\n")
	output_file.write("\\begin{tabular}{c}\n")
	if(platform.system() == "Windows"):
			prefix = "C:/Users/PC_immuno/Desktop/Nathan/SpellCraft/HOLIDAYS/"
			image = prefix + "output/images/LDA_visualisation"
	else:
		image = "output/images/LDA_visualisation"
	if(os.path.exists(image)):
		output_file.write("\\includegraphics[scale=0.5]{\""+str(image)+"\"}\\\\ \n")
	else:
		output_file.write("Image not found\\\\ \n")
	output_file.write("scatterplot of the best two discriminant functions\n")
	output_file.write("\\end{tabular}\n")
	output_file.write("\\end{center}\n")

   	## Write footer
   	output_file.write("\\end{document}")
	output_file.close()




def compile_report(tex_file_name):
	"""
	-> Create a pdf file from the tex file.
	-> Delete the tex file and all log, aux files
	   generated during the compilation
	-> move pdf file in output/reports folder
	"""	

	if(platform.system() == "Windows"):

		## Compile with pdflatex
		os.system("pdflatex " +str(tex_file_name))

		## remove .aux files
		file_to_remove = glob.glob("*.aux")
		for f in file_to_remove:
			os.remove(f)

		## remove .log files
		file_to_remove = glob.glob("*.log")
		for f in file_to_remove:
			os.remove(f)

		## delete tex file
		os.remove(tex_file_name)

		## Move pdf file
		pdf_file_destination = tex_file_name.replace(".tex", ".pdf")
		pdf_file = tex_file_name.split("/")
		pdf_file = pdf_file[-1]
		pdf_file = pdf_file.replace(".tex", ".pdf")
		shutil.copy(pdf_file, pdf_file_destination)
		os.remove(pdf_file)


	elif(platform.system() == "Linux"):
		
		 ## Compile with rubber
		 os.system("rubber -q --pdf "+str(tex_file_name))

		 ## remove .aux files
		 file_to_remove = glob.glob("*.aux")
		 for f in file_to_remove:
		 	os.remove(f)

		 ## remove .log files
		 file_to_remove = glob.glob("*.log")
		 for f in file_to_remove:
		 	os.remove(f)

		 ## delete tex file
		 os.remove(tex_file_name)

		 ## Move pdf file
		 pdf_file_destination = tex_file_name.replace(".tex", ".pdf")
		 pdf_file = tex_file_name.split("/")
		 pdf_file = pdf_file[-1]
		 pdf_file = pdf_file.replace(".tex", ".pdf")
		 shutil.copy(pdf_file, pdf_file_destination)
		 os.remove(pdf_file)



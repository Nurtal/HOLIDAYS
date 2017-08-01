
## RUN AFD ANALYSIS


## Assume the predictive variable always gone a be the first column

## TODO:
## Absolute path gestion -> find a way to use relative path to data file
## Find a way to extract the explicative value (Diagnostic) for formula in lda
## Fix path for windows installation

##-----------##
## LOAD DATA ##
##-----------##

## turn of warnings
options(warn=-1)

## Where am i 
info = Sys.info()
os = info[["sysname"]]
data_file_name = "undef"
login = info[["login"]]

## Load data on Windows
if(identical(os, "Windows")){
  
  ## input file name
  data_file_name = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\CBFD\\data\\pca_exploration\\pca_exploration_input.csv", sep="")
  
  ## output file name
  png_path_overview = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\HOLIDAYS\\input\\output\\", sep="")
  lda_prior_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\HOLIDAYS\\input\\output\\lda_prior_file.csv", sep="")
  lda_count_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\BIOTOOLBOX\\input\\output\\lda_count_file.csv", sep="")
  lda_number_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\BIOTOOLBOX\\input\\output\\lda_number_file.csv", sep="")
  lda_means_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\BIOTOOLBOX\\input\\output\\lda_means_file.csv", sep="")
  lda_scaling_file = paste("C:\\Users\\", login, "\\Desktop\\Nathan\\SpellCraft\\BIOTOOLBOX\\input\\output\\lda_scaling_file.csv", sep="")
  
  ## Load data on Linux
}else{
  
  ## input file name
  data_file_name = paste("/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/data/data.csv", sep="")
  
  ## output file name
  png_path_overview = "/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/output/images/"
  lda_prior_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/output/lda_prior_file.csv"
  lda_count_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/output/lda_count_file.csv"
  lda_number_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/output/lda_number_file.csv"
  lda_means_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/output/lda_means_file.csv"
  lda_scaling_file = "/home/foulquier/Bureau/SpellCraft/WorkSpace/Github/HOLIDAYS/output/lda_scaling_file.csv"
  
  
}
data = read.csv(data_file_name, stringsAsFactors=TRUE, sep=",")
attach(data)

##-----------------##
## IMPORT PACKAGES ##
##-----------------##
library(car)
library(MASS)


##---------------##
## DATA OVERVIEW ##
##---------------##

## Scatter plot -> overview of the data
## Warnings but seems to work
max_display = 10
total_size = ncol(data)
if((total_size-1) <= max_display){
  png_save_file = paste(png_path_overview, "scatterplot_complete.png", sep="")
  png(filename=png_save_file)
  scatterplotMatrix(data[2:ncol(data)])
  dev.off()
}else{
  last_iteration = 2
  iteration = 2
  while(iteration <= total_size){
    if(iteration + max_display <= total_size){
      last_iteration = iteration
      iteration = iteration + max_display
      png_save_file = paste(png_path_overview, "scatterplot_var", last_iteration, "_from_var", iteration,".png" , sep="")
      png(filename=png_save_file)
      scatterplotMatrix(data[last_iteration:iteration])
      dev.off()
    }else{
      last_iteration = iteration
      iteration = ncol(data)
      last_iteration
      png_save_file = paste(png_path_overview, "scatterplot_var", last_iteration, "_from_var", iteration,".png" , sep="")
      png(filename=png_save_file)
      scatterplotMatrix(data[last_iteration:ncol(data)])
      dev.off()
      iteration = iteration + 1 # break the loop
    }
  }
}


##--------------##
## LDA analysis ##
##--------------##

## Perform LDA
data.lda <- lda(Diagnostic ~ ., data=data) ## Formula to fix

## Write LDA informations
write.table(data.lda$prior, file=lda_prior_file, sep=",")
write.table(data.lda$counts, file=lda_count_file, sep=",")
write.table(data.lda$N, file=lda_number_file, sep=",")
write.table(data.lda$means, file=lda_means_file, sep=",")
write.table(data.lda$scaling, file=lda_scaling_file, sep=",")

## Plot LDA results
data.lda.values <- predict(data.lda)
comp = 1
while(comp <= ncol(data.lda$scaling)){
  png_save_file = paste(png_path_overview, "LDA_", comp, "_histogram.png" , sep="")
  png(filename=png_save_file)
  ldahist(data = data.lda.values$x[,comp], g=Diagnostic) ## Formula to fix (g arguments)
  dev.off()
  comp = comp + 1
}

## Scatterplots of the Discriminant Functions
png_save_file = paste(png_path_overview, "LDA_visualisation.png" , sep="")
png(filename=png_save_file)
plot(data.lda.values$x[,1],data.lda.values$x[,2]) # make a scatterplot
text(data.lda.values$x[,1],data.lda.values$x[,2],Diagnostic,cex=0.7,pos=4,col="red") ## fix Diagnostc problem
dev.off()

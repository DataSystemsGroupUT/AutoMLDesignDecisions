library(SmartML)
library(reticulate)

timeBudget <- 60
dir <- '/home/maher/datasets/'
datasets <- setdiff(list.files(dir), list.dirs(recursive = FALSE, full.names = FALSE))
datasets <- sort(datasets)
print(datasets)
i <- 1
while(i < 31){
  gc()
  testData <- paste(dir, datasets[i], sep = '')
  trainData <- paste(dir, datasets[i+1], sep = '')
  i <- i + 2

  cat('Train Data:', trainData)

  con <- file(testData, "r")
  tesData <- read.csv(file = con, header = TRUE, sep = ",", stringsAsFactors = FALSE)
  close(con)

  classCol <- colnames(tesData)
  res2 <- list()
  #### BEGIN of Logging
  print(getwd())
  #pid <- Sys.getpid()
  #cmdPy <- paste("python openLoggers.py", toString(pid), datasets[i-1], sep = ' ')
  #system(cmdPy, wait=FALSE)

  benchmarkError <- try(
  {
    res <- autoRLearn(timeBudget, trainData, testData, classCol = classCol[length(classCol)], nModels = 5, metric = 'fscore')
    testPerf <- res$perf
    res2 <- runClassifier(trainingSet = res$TRData, validationSet = res$TRData, params = res$params, classifierAlgorithm = res$clfs, interp = FALSE)
  })
  if(inherits(benchmarkError, "try-error")){
    testPerf <- NA
    res2$perf <- NA
    res$clfs <- NA
  }

  #system("python closeLoggers.py", wait=TRUE)
  #### END of Logging

  CollectResults <- paste(trainData, res$clfs, 'acc', res2$perf, testPerf, sep = ',')
  print(CollectResults)
  write(CollectResults, file="/home/maher/result.csv",append=TRUE)
}

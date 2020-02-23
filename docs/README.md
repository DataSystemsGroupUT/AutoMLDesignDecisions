# AutoML Micro Analysis
In this study, we focus on the Microlevel by empirically evaluating and analyzing the performance impact of several design decisions and parameters including meta-learning,ensembling,time budget and size of search space,separately and combined. The results of our study reveal various interesting insights that can significantly guide and impact the design of AutoML frameworks.
* [Benchmark Datasets](#benchmark-datasets)
* [Experiment Setup](#experimental-setup)
* [Results](#results)
  * Impact of Meta-learning 
  * Impact of Ensembling 
  * Impact of Time Budget 

## Benchmark Datasets
We used 100 datasets from [OpenML](https://www.openml.org/) repository. We selected them to cover different characteristics of datasets including the number of classes, number of instances, number of features, etc.

### List of the datasets

| Dataset ID    | Dataset URL   | #features   | #instances   | #classes     |
| ---| --- |--- | --- | --- |
|aaaData_for_UCI_named|[-](-)|14|10000|2|
|AirlinesCodrnaAdult|[https://www.openml.org/d/1240](https://www.openml.org/d/1240)|30|1076790|2|
|Amazon|[https://www.openml.org/d/1457](https://www.openml.org/d/1457)|10001|1500|50|
|analcatdata_authorship|[https://www.openml.org/d/458](https://www.openml.org/d/458)|71|841|4|
|AP_Breast_Lung|[https://www.openml.org/d/1150](https://www.openml.org/d/1150)|10937|470|2|
|AP_Omentum_Ovary|[https://www.openml.org/d/1156](https://www.openml.org/d/1156)|10937|275|2|
|AP_Prostate_Ovary|[https://www.openml.org/d/1152](https://www.openml.org/d/1152)|10937|267|2|
|arrhythmia|[https://www.openml.org/d/1017](https://www.openml.org/d/1017)|263|452|2|
|audiology|[https://www.openml.org/d/999](https://www.openml.org/d/999)|70|226|2|
|avila-tr|[https://archive.ics.uci.edu/ml/machine-learning-databases/00459/](https://archive.ics.uci.edu/ml/machine-learning-databases/00459/)|11|20867|12|
|churn|[https://www.openml.org/d/40701](https://www.openml.org/d/40701)|21|5000|2|
|cifar-10|[https://www.openml.org/d/40927](https://www.openml.org/d/40927)|3073|60000|10|
|connect-4|[https://www.openml.org/d/1591](https://www.openml.org/d/1591)|43|67557|3|
|CovPokElec|[https://www.openml.org/d/149](https://www.openml.org/d/149)|65|1455525|10|
|dataset_183_adult|[https://www.openml.org/d/179](https://www.openml.org/d/179)|15|48842|2|
|dataset_185_yeast|[https://www.openml.org/d/181](https://www.openml.org/d/181)|9|1484|10|
|dataset_186_satimage|[https://www.openml.org/d/182](https://www.openml.org/d/182)|37|6430|6|
|dataset_187_abalone|[https://www.openml.org/d/183](https://www.openml.org/d/183)|9|4177|28|
|dataset_189_baseball|[https://www.openml.org/d/185](https://www.openml.org/d/185)|18|1340|3|
|dataset_194_eucalyptus|[https://www.openml.org/d/188](https://www.openml.org/d/188)|20|736|5|
|dataset_24_mushroom|[https://www.openml.org/d/24](https://www.openml.org/d/24)|22|8124|2|
|dataset_26_nursery|[https://www.openml.org/d/26](https://www.openml.org/d/26)|9|12960|5|
|dataset_28_optdigits|[https://www.openml.org/d/28](https://www.openml.org/d/28)|63|5620|10|
|dataset_31_credit-g|[https://www.openml.org/d/31](https://www.openml.org/d/31)|21|1000|2|
|dataset_36_segment|[https://www.openml.org/d/36](https://www.openml.org/d/36)|19|2310|7|
|dataset_39_ecoli|[https://www.openml.org/d/39](https://www.openml.org/d/39)|8|336|8|
|dataset_40_sonar|[https://www.openml.org/d/40](https://www.openml.org/d/40)|61|208|2|
|dataset_42_soybean|[https://www.openml.org/d/42](https://www.openml.org/d/42)|36|683|19|
|dataset_44_spambase|[https://www.openml.org/d/44](https://www.openml.org/d/44)|58|4601|2|
|dataset_54_vehicle|[https://www.openml.org/d/54](https://www.openml.org/d/54)|19|846|4|
|dataset_59_ionosphere|[https://www.openml.org/d/59](https://www.openml.org/d/59)|34|351|2|
|dataset_6_letter|[https://www.openml.org/d/6](https://www.openml.org/d/6)|17|20000|26|
|dataset_60_waveform-5000|[https://www.openml.org/d/60](https://www.openml.org/d/60)|41|5000|3|
|dataset_61_iris|[https://www.openml.org/d/61](https://www.openml.org/d/61)|5|150|3|
|dataset_9_autos|[https://www.openml.org/d/9](https://www.openml.org/d/9)|26|205|6|
|devnagari|[https://www.openml.org/d/40923](https://www.openml.org/d/40923)|785|92000|46|
|electricity-normalized|[https://www.openml.org/d/151](https://www.openml.org/d/151)|9|45312|2|
|eye_movements|[https://www.openml.org/d/1044](https://www.openml.org/d/1044)|28|10936|3|
|GCM|[https://www.openml.org/d/1106](https://www.openml.org/d/1106)|16064|190|14|
|gina_agnostic|[https://www.openml.org/d/1038](https://www.openml.org/d/1038)|971|3468|2|
|hiva_agnostic|[https://www.openml.org/d/1039](https://www.openml.org/d/1039)|1618|4229|2|
|ipums_la_99-small|[https://www.openml.org/d/378](https://www.openml.org/d/378)|60|8844|9|
|jm1|[https://www.openml.org/d/1053](https://www.openml.org/d/1053)|22|10885|2|
|jungle_chess_2pcs|[https://www.openml.org/d/40997](https://www.openml.org/d/40997)|45|4704|3|
|KDDCup99|[https://www.openml.org/d/1113](https://www.openml.org/d/1113)|40|494020|23|
|kin8nm|[https://www.openml.org/d/189](https://www.openml.org/d/189)|9|8192|2|
|leukemia|[https://www.openml.org/d/1104](https://www.openml.org/d/1104)|7130|72|2|
|lymphoma_2classes|[https://www.openml.org/d/1101](https://www.openml.org/d/1101)|4027|45|2|
|MagicTelescope|[https://www.openml.org/d/1120](https://www.openml.org/d/1120)|11|19020|2|
|mfeat-pixel|[https://www.openml.org/d/20](https://www.openml.org/d/20)|241|2000|2|
|mnist_784|[https://www.openml.org/d/554](https://www.openml.org/d/554)|720|70000|10|
|openml_phpJNxH0q|[https://www.openml.org/d/15](https://www.openml.org/d/15)|10|699|2|
|page-blocks|[https://www.openml.org/d/30](https://www.openml.org/d/30)|11|5473|2|
|php0FyS2T|[https://www.openml.org/d/1492](https://www.openml.org/d/1492)|65|1600|100|
|php3CTpvq|[https://www.openml.org/d/1509](https://www.openml.org/d/1509)|5|149332|22|
|php5OMDBD|[https://www.openml.org/d/40971](https://www.openml.org/d/40971)|23|1000|30|
|php5s7Ep8|[https://www.openml.org/d/40982](https://www.openml.org/d/40982)|28|1941|7|
|php7KLval|[https://www.openml.org/d/1547](https://www.openml.org/d/1547)|21|1000|2|
|phpB0xrNj|[https://www.openml.org/d/300](https://www.openml.org/d/300)|618|7797|26|
|phpbL6t4U|[https://www.openml.org/d/1476](https://www.openml.org/d/1476)|129|13910|6|
|phpchCuL5|[https://www.openml.org/d/40966](https://www.openml.org/d/40966)|81|1080|8|
|phpCsX3fx|[https://www.openml.org/d/1491](https://www.openml.org/d/1491)|65|1600|100|
|phpdo58hj|[https://www.openml.org/d/1562](https://www.openml.org/d/1562)|4703|64|2|
|phpdReP6S|[https://www.openml.org/d/1487](https://www.openml.org/d/1487)|73|2534|2|
|phpEZ030X|[https://www.openml.org/d/1561](https://www.openml.org/d/1561)|3722|64|2|
|phpfLuQE4|[https://www.openml.org/d/1485](https://www.openml.org/d/1485)|501|2600|2|
|phpfrJpBS|[https://www.openml.org/d/1568](https://www.openml.org/d/1568)|9|12958|4|
|phpGReJjU|[https://www.openml.org/d/40985](https://www.openml.org/d/40985)|4|45781|20|
|phpGUrE90|[https://www.openml.org/d/1494](https://www.openml.org/d/1494)|42|1055|2|
|phphQEck0|[https://www.openml.org/d/1502](https://www.openml.org/d/1502)|4|245057|2|
|phpHyLSNF|[https://www.openml.org/d/1515](https://www.openml.org/d/1515)|1083|571|20|
|phpkIxskf|[https://www.openml.org/d/1461](https://www.openml.org/d/1461)|17|45211|2|
|phpmcGu2X|[https://www.openml.org/d/1468](https://www.openml.org/d/1468)|857|1080|9|
|phpmPOD5A|[https://www.openml.org/d/4135](https://www.openml.org/d/4135)|10|32769|2|
|phpn1jVwe|[https://www.openml.org/d/310](https://www.openml.org/d/310)|7|11183|2|
|phpN4gaxw|[https://www.openml.org/d/1477](https://www.openml.org/d/1477)|130|13910|6|
|phpNevWWL|[https://www.openml.org/d/40477](https://www.openml.org/d/40477)|27|2800|5|
|phpoOxxNn|[https://www.openml.org/d/1493](https://www.openml.org/d/1493)|65|1599|100|
|phpoW7Dbi|[https://www.openml.org/d/1566](https://www.openml.org/d/1566)|101|1212|2|
|phpPbCMyg|[https://www.openml.org/d/1475](https://www.openml.org/d/1475)|52|6118|6|
|phprAeXmK|[https://www.openml.org/d/4535](https://www.openml.org/d/4535)|42|299285|2|
|phpSZJq5T|[https://www.openml.org/d/1514](https://www.openml.org/d/1514)|1088|360|10|
|phptd5jYj|[https://www.openml.org/d/1501](https://www.openml.org/d/1501)|37|5100|2|
|phpTJRsqa|[https://www.openml.org/d/40498](https://www.openml.org/d/40498)|257|1593|10|
|phpvcoG8S|[https://www.openml.org/d/1169](https://www.openml.org/d/1169)|12|4898|7|
|phpVeNa5j|[https://www.openml.org/d/1497](https://www.openml.org/d/1497)|8|539383|2|
|phpvtdNPU|[https://www.openml.org/d/1079](https://www.openml.org/d/1079)|25|5456|4|
|phpWfYmlu|[https://www.openml.org/d/1496](https://www.openml.org/d/1496)|21|7400|2|
|phpxijhaP|[https://www.openml.org/d/1507](https://www.openml.org/d/1507)|22278|95|5|
|phpYLeydd|[https://www.openml.org/d/4538](https://www.openml.org/d/4538)|21|7400|2|
|phpZrCzJR|[https://www.openml.org/d/40900](https://www.openml.org/d/40900)|33|9873|5|
|pokerhand-normalized|[https://www.openml.org/d/155](https://www.openml.org/d/155)|11|829201|10|
|schizo|[https://www.openml.org/d/466](https://www.openml.org/d/466)|14|340|2|
|shuttle|[https://www.openml.org/d/40685](https://www.openml.org/d/40685)|10|58000|7|
|solar-flare_1|[https://www.openml.org/d/40686](https://www.openml.org/d/40686)|13|315|5|
|synthetic_control|[https://www.openml.org/d/377](https://www.openml.org/d/377)|61|600|6|
|tumors_C|[https://www.openml.org/d/1107](https://www.openml.org/d/1107)|7130|60|2|
|umistfacescropped|[https://www.openml.org/d/41084](https://www.openml.org/d/41084)|10305|575|20|
|vowel|[https://www.openml.org/d/307](https://www.openml.org/d/307)|14|990|2|
|wine-quality-red|[https://www.openml.org/d/40691](https://www.openml.org/d/40691)|12|1599|6|

## Experimental Setup

Our experiments have been conducted on Google Cloud machines, each machine is configured with 2 vCPUs, 7.5 GB RAM and ubuntu-minimal-1804-bionic. we used the 100 datasets. For our study, we have run each experiment 4 times with 4 different time budgets: 10, 30, 60 and 240 minutes. We have used AutoSklearn, the winner of two ChaLearn AutoML challenges, as our experimental AutoML framework.

AutoSklearn is implemented on top of Scikit-Learn, a popular Python machine learning package. AutoSklearn uses Sequential Model-based  Algorithm Configuration (SMAC) as a Bayesian optimization technique. AutoSklearn allows the end-users to enable/disable the different optimization options including using of meta-learning (AutoSKLearn-m), ensembling (AutoSKLearn-e) in addition  to  the  full  version  where  all  options  are  enabled.

## Results

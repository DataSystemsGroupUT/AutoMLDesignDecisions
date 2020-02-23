# AutoML Micro Analysis
In this study, we focus on the Microlevel by empirically evaluating and analyzing the performance impact of several design decisions and parameters including meta-learning,ensembling,time budget and size of search space,separately and combined. The results of our study reveal various interesting insights that can significantly guide and impact the design of AutoML frameworks.

## Benchmark Datasets
### List of the datasets

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |


| Dataset ID    | Dataset URL   | # features   | # instances   | # classes     |
| ---| --- |--- | --- | --- |
|     audiology   | https://www.openml.org/d/999 |70| 226  |2|
|     arrhythmia   | https://www.openml.org/d/999 |280 | 452  |2|
|     AP_Breast_Lung  |https://www.openml.org/d/1150|10937 | 470  |2|
|     openml_phpJNxH0q     | https://www.openml.org/d/15  |10 | 699  |2  |
|     Vowel     | https://www.openml.org/d/1016  |14 | 990  |2  |
|     dataset_31_credit-g     | https://www.openml.org/d/31 |21| 1000  |2  |
|     gina_agnostic  |https://www.openml.org/d/1038|971 | 3468  |2|
|     hiva_agnostic  |https://www.openml.org/d/1039|1618 | 4229  |2|
|     phpZrCzJR  |https://www.openml.org/d/1039|37 | 5100  |2|
|     MagicTelescope    | https://www.openml.org/d/1120 |12| 19020  |2|
|     electricity-normalized    | https://www.openml.org/d/151 |9| 45312  |2|
|     AirlinesCodrnaAdult    | https://www.openml.org/d/1240  |30| 1076790  |2|
|     eye_movements   | https://www.openml.org/d/1044 |28| 10936  |3|
|     connect-4  |https://www.openml.org/d/40668|43 | 67557  |3|
|     solar-flare_1     | https://www.openml.org/d/40686  |13| 315  |5  |
|     wine-quality-red    | https://www.openml.org/d/40691  |12| 1599  |6 |
|     pokerhand-normalized    | https://www.openml.org/d/155 |11| 829201  |10|
|     umistfacescropped  |https://www.openml.org/d/41084|10305 | 575  |20|
|     KDDCup99  |https://www.openml.org/d/1113|42 | 494020  |23|
|     Amazon  |https://www.openml.org/d/1150|10001 | 1500  |50|

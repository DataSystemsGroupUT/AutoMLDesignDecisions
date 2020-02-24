# AutoML Micro Analysis
In this study, we focus on the Microlevel by empirically evaluating and analyzing the performance impact of several design decisions and parameters including meta-learning,ensembling,time budget and size of search space,separately and combined. The results of our study reveal various interesting insights that can significantly guide and impact the design of AutoML frameworks.
* [Benchmark Datasets](https://datasystemsgrouput.github.io/AutoMLMicroAnalysis/datasets)
* [Experiment Setup](#experimental-setup)
* [Results](#results)
  * Impact of Meta-learning 
  * Impact of Ensembling 
  * Impact of Time Budget 


## Experimental Setup

Our experiments have been conducted on Google Cloud machines, each machine is configured with 2 vCPUs, 7.5 GB RAM and ubuntu-minimal-1804-bionic. we used the 100 datasets. For our study, we have run each experiment 4 times with 4 different time budgets: 10, 30, 60 and 240 minutes. We have used AutoSklearn, the winner of two ChaLearn AutoML challenges, as our experimental AutoML framework.

AutoSklearn is implemented on top of Scikit-Learn, a popular Python machine learning package. AutoSklearn uses Sequential Model-based  Algorithm Configuration (SMAC) as a Bayesian optimization technique. AutoSklearn allows the end-users to enable/disable the different optimization options including using of meta-learning (AutoSKLearn-m), ensembling (AutoSKLearn-e) in addition  to  the  full  version  where  all  options  are  enabled.

## Results
![test](https://raw.githubusercontent.com/DataSystemsGroupUT/AutoMLMicroAnalysis/master/docs/data/006MetaLearningEffectAll10min.png)


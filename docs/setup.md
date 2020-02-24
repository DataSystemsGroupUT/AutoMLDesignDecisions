## Experimental Setup

Our experiments have been conducted on Google Cloud machines, each machine is configured with 2 vCPUs, 7.5 GB RAM and ubuntu-minimal-1804-bionic. we used the 100 datasets. For our study, we have run each experiment 4 times with 4 different time budgets: 10, 30, 60 and 240 minutes. We have used AutoSklearn, the winner of two ChaLearn AutoML challenges, as our experimental AutoML framework.

AutoSklearn is implemented on top of Scikit-Learn, a popular Python machine learning package. AutoSklearn uses Sequential Model-based  Algorithm Configuration (SMAC) as a Bayesian optimization technique. AutoSklearn allows the end-users to enable/disable the different optimization options including using of meta-learning (AutoSKLearn-m), ensembling (AutoSKLearn-e) in addition  to  the  full  version  where  all  options  are  enabled.

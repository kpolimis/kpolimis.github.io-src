---
Title: Software
sortorder: 003
---
# Forest-Confidence-Interval 
Developed with Ariel Rokem and  Bryna Hazelton from eScience Institute, University of Washington

# Summary
Random forests are a method for predicting numerous ensemble learning tasks. The variability in predictions is important for measuring standard errors and estimating standard errors. Forest-Confidence-Interval is a Python module for calculating variance and adding confidence intervals to scikit-learn random forest regression or classification objects. The core functions calculate an in-bag and error bars for random forest objects. This module is an implementation of an algorithm developed by Wager, Hastie and Efron (2014) and previously implemented in R here (Wager 2016).

# Examples gallery
## Regression example
![plot-mpg](../../images/plot_mpg.png)

## Classification example
![plot-spam](../../images/plot_spam.png)


# References

Wager, Stefan. 2016. "randomForestCI". [Github](September. https://github.com/swager/randomForestCI).

Wager, Stefan, Trevor Hastie, and Bradley Efron. 2014. "Confidence Intervals for Random Forests: The Jackknife and the Infinitesimal Jackknife".The Journal of Machine Learning Research 15 (1): 1625-51.

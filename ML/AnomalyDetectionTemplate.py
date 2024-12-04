"""
Anomaly Detection is a technique used to identify 
unusual patterns that do not conform to expected behavior, called outliers.
It has many applications in business, 
from fraud detection in credit card transactions to fault detection in operating environments.

After the learning algorithm sees a data set in which
the system is operating normally, it can detect any deviation from this normal behavior.

Does the new data set contain any anomalies?


First step you build a probability model of X.
The learning algorithm will try to figure out what are the values 
of the features x1 and x2 that have high probability and what are 
the values that are less likely or have a lower chance or lower probability 
of being seen in the data set. 

PCA-Based Anomaly detection would be a better choice for detecting 
a mouse jiggler script since it answers the question: Is this weird?
instead of a classification algorithm that answers the question: What is this, A or B?

Gaussian Distribution/Normal Distribution/Bell shaped distribution
is a probability distribution that is symmetric about the mean,
showing that data near the mean are more frequent in occurrence than data far from the mean.

p(x) = 1/(sqrt(2*pi)*sigma) * exp(-((x-mu)^2)/(2*sigma^2))

if p(x) < epsilon, then it is an anomaly. But that's only for one feature.

Trainig set: {Vector x1, x2, x3, ..., xm}
Each example X(i) is a vector with n features.

P(Vector x) = P(x1; mu1; sigma1^2) * P(x2; mu2; sigma2^2) * ... * P(xn; mun; sigman^2)
mu is the mean of the training set
sigma^2 is the variance of the training set

Steps:
1. Choose features x(i) that you think might be indicative of anomalous examples.
2. Fit parameters mu1, ..., mun, sigma1^2, ..., sigman^2 ( Remember: mu is the mean and sigma^2 is the variance)
3. Compute p(x)
4. Anomaly if p(x) < epsilon

Epislon can be a threshold value that you can tune to get the best results.
For example it can be a percentile like 90th or 95th percentile.

When developing a learning algorithm, making decisions about fine tuning parameters
is much easier if we have a way of evaluating the algorithm. 
( Real-number evaluation - computing a number which tells us how well the algorithm is doing)

Possible features to be used:
- Speed of the mouse
- Distance between two consecutive points

"""
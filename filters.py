import numpy as np

# Does not do anything to the eigenvalue, just multiplies them by 1 for testing purposes
def h(x):
    return (1 * x)

#------------------------------------------------------------------------
# LOW PASS FILTERS
#------------------------------------------------------------------------

# Low pass filter that was defined in the PyGSP documentation
def lp1(x):
    tau = 1
    return 1. / (1. + tau * x)

# Low pass filter that uses a negative cubic function, suggested parameters
# are a = 1, and b = 1/(G.lmax) where G.lmax is the max eigenvalue for the graph
a = 1
b = 1/G.lmax
def lp2(x):
    return((a - (b*x))**3)


# Trivial low pass filter, keeps frequenccies below a certain cutoff point
def lp3(x):
    q = 1
    y = np.zeros(len(x))
    for i in range(len(x)):
        if(x[i] < q):
            y[i] = 1
        else:
            y[i] = 0
    return(y)

#------------------------------------------------------------------------
# HIGH PASS FILTERS
#------------------------------------------------------------------------

# Trivial high pass filter, keeps frequencies above a certain cutoff point
def hp1(x):
    q = 1
    y = np.zeros(len(x))
    for i in range(len(x)):
        if(x[i] < q):
            y[i] = 0
        else:
            y[i] = 1
    return(y)

# Smoother high pass filter, it is the negation of the PyGSP filter shifted up by 1
def hp2(x):
    tau = 1
    return((-1. / (1. + tau * x)) + 1)

# Negation of the lp2 filter and shifted upwards by 1. The parameters here are still
# the same, a = 1, and b = 1/(G.lmax) where G.lmax is the max eigenvalue for the graph
a = 1
b = 1/G.lmax
def hp3(x):
    return(-(a - (b*x))**3 + 1)

#------------------------------------------------------------------------
# RATIONAL FILTERS
#------------------------------------------------------------------------

# Rational low pass filter that was proposed by this thesis
def rl(x):
    a = 1
    b = 0.125
    return(((a - (b*x))**3) / ((1 + b*x) + (b**2 * x**2) + (b**3 * x**3)))

# Rational high pass filter that as proposed by this thesis
def rh(x):
    a = 1
    b = 0.125
    return((-(a - (b*x))**3) / ((1 + b*x) + (b**2 * x**2) + (b**3 * x**3)) + 1)

#------------------------------------------------------------------------
# BAND PASS FILTERS
#------------------------------------------------------------------------


# This is smooth "hat" filter, it keeps the eigenvalues in the middle of the spectrum,
# while it reduces those towards the ends. It requires the calculation of the max
# eigenvalue for the Graph, in order to find the center of the spectrum. Each end of
# the "hat" is at 0 (lambda_0) and at lambda_max. This filter was not utilized in the
# thesis paper, but was one of the filters that was tested
# ------------------------
# center = Q.lmax/2
# a = 1/(center)**n
# ------------------------
def bq2(x):
    return(-a*(x - center)**2 + 1)


# This is a windowed "hat" filter. It zeros the eigenvalues that are in the first and
# last quarter of the spectrum, and keeps the middle 50% of eigenvalues. It has a steep
# cutoff between the values that are kept and discarded
# ------------------------
# center = Q.lmax/2
# a = center/(Q.lmax*2)
# ------------------------
def tb1(x):
    y = np.zeros(len(x))
    for i in range(0,len(x)):
        if((x[i] < (center/2)) or (x[i] > (center + (center/2)))):
            y[i] = 0
        else:
            y[i] = 1
    return(y)

# Same as above, except it keeps the values on the ends and discards the values in the middle
#
# ------------------------
# center = Q.lmax/2
# a = center/(Q.lmax*2)
# ------------------------
def tb2(x):
    y = np.zeros(len(x))
    for i in range(0,len(x)):
        if((x[i] < (center/2)) or (x[i] > (center + (center/2)))):
            y[i] = 1
        else:
            y[i] = 0
    return(y)

# This filter is somewhat of a mix of the functions bq2 and tb1. It cuts off the values for
# the first and last quarter of the spectrum, but keeps the values in the middle. Instead
# of having a sharp jump up to 1, there is instead a negative quadratic similar to bq2,
# with each end at 25th and 75th percentile of the eigenvalues. This is the BQ filter
# discussed in the paper
#
# ------------------------
# center = Q.lmax/2
# a = 1/(center/2)**n
# ------------------------
def bq(x):
    y = np.zeros(len(x))
    for i in range(0,len(x)):
        if((x[i] < (center/2)) or (x[i] > (center + (center/2)))):
            y[i] = 0
        else:
            y[i] = -a*(x[i] - center)**2 + 1
    return(y)
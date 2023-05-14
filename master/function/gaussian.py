
# coding: utf-8

# # Function iagaussian

# ## Synopse

# Generate a d-dimensional Gaussian image.
# 
# - **g = gaussian(s, mu, cov)**
# 
#   - **g**: Image. 
# 
# 
#   - **s**: Image shape. (rows columns)
#   - **mu**: Image. Mean vector. n-D point. Point of maximum value.
#   - **cov**: Covariance matrix (symmetric and square).

# In[3]:

import numpy as np

def gaussian(s, mu, cov):
    d = len(s)  # dimension
    n = np.prod(s) # n. of samples (pixels)
    x = np.indices(s).reshape( (d, n))
    xc = x - mu 
    k = 1. * xc * np.dot(np.linalg.inv(cov), xc)
    k = np.sum(k,axis=0) #the sum is only applied to the rows
    g = (1./((2 * np.pi)**(d/2.) * np.sqrt(np.linalg.det(cov)))) * np.exp(-1./2 * k)
    return g.reshape(s)


# ## Description

# A n-dimensional Gaussian image is an image with a Gaussian distribution. It can be used to generate 
# test patterns or Gaussian filters both for spatial and frequency domain. The integral of the gaussian function is 1.0.

# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python gaussian.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia
    
    get_ipython().magic('matplotlib inline')
    import matplotlib.pyplot as plt


# ### Example 1 - Numeric 2-dimensional

# In[2]:

if testing:
    f = ia.gaussian((8, 4), np.transpose([[3, 1]]), [[1, 0], [0, 1]])
    print('f=\n', np.array2string(f, precision=4, suppress_small=1))
    g = ia.normalize(f, [0, 255]).astype(np.uint8)
    print('g=\n', g)


# ## Example 2 - one dimensional signal

# In[3]:

# note that for 1-D case, the tuple has extra ,
# and the covariance matrix must be 2-D
if testing:
    f = ia.gaussian( (100,), 50, [[10*10]]) 
    g = ia.normalize(f, [0,1])
    plt.plot(g)
    plt.show()


# ### Example 3 - two-dimensional image

# In[4]:

if testing:
    f = ia.gaussian((150,250), np.transpose([[75,100]]), [[40*40,0],[0,30*30]])
    g = ia.normalize(f, [0,255]).astype(np.uint8)
    ia.adshow(g)


# ## Example 4 - Numeric 3-dimensional

# In[6]:

if testing:
    f = ia.gaussian((3,4,5), np.transpose([[1,2,3]]), [[1,0,0],[0,4,0],[0,0,9]])
    print('f=\n', np.array2string(f, precision=4, suppress_small=1))
    g = ia.normalize(f, [0,255]).astype(np.uint8)
    print('g=\n', g)


# ## Equation

# $$    f(x) = \frac{1}{\sqrt{2 \pi} \sigma} exp\left[ -\frac{1}{2} \left( \frac{x - \mu}{\sigma} \right)^2 \right]
# $$
# 
# $$ f({\bf x}) = \frac{1}{(2 \pi)^{d/2}|\Sigma|^{1/2}} exp\left[ -\frac{1}{2}\left({\bf x} - \mu \right)^t\Sigma^{-1}\left({\bf x} - \mu \right)\right]
# $$

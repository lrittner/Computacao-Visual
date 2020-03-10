
# coding: utf-8

# # Function h2percentile
# 
# ## Synopse
# 
# The *h2percentile* function computes the percentile given an image histogram.
# 
# - **g = iapercentile(h,q)**
#     - **Output**
#         - **g**: percentile value(s)
#       
#     - **Input**
#         - **h**: 1D ndarray: histogram
#         - **q**: 1D float ndarray in range of [0,100]. Default value = 1.
#     
# ## Description
# 
# The *h2percentile* function computes the percentiles from a given histogram.
# 
# ## Function Code

# In[ ]:

def h2percentile(h,p):

    import numpy as np
    s = h.sum()
    k = ((s-1) * p/100.)+1
    dw = np.floor(k)
    up = np.ceil(k)
    hc = np.cumsum(h)
    if isinstance(p, int):
        k1 = np.argmax(hc>=dw)
        k2 = np.argmax(hc>=up)
    else:   
        k1 = np.argmax(hc>=dw[:,np.newaxis],axis=1)
        k2 = np.argmax(hc>=up[:,np.newaxis],axis=1)
    d0 = k1 * (up-k)
    d1 = k2 * (k -dw)
    return np.where(dw==up,k1,d0+d1)     


# ## Examples

# In[1]:

testing = (__name__ == "__main__")

if testing:
    get_ipython().system(' jupyter nbconvert --to python h2percentile.ipynb')
    import numpy as np
    import sys,os
    import matplotlib.image as mpimg
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Numeric Example
# 
# Comparison with the NumPy percentile implementation:
# 
# 

# In[2]:

if testing:
    f = np.array([0,1,2,3,4,5,6,7,8])
    h = ia.histogram(f)
    print('h2percentile  1 = %f, np.percentile  1 = %f'%(ia.h2percentile(h,1),np.percentile(f,1)))
    print('h2percentile 10 = %f, np.percentile 10 = %f'%(ia.h2percentile(h,10),np.percentile(f,10)))
    print('h2percentile 50 = %f, np.percentile 50 = %f'%(ia.h2percentile(h,50),np.percentile(f,50)))
    print('h2percentile 90 = %f, np.percentile 90 = %f'%(ia.h2percentile(h,90),np.percentile(f,90)))
    print('h2percentile 99 = %f, np.percentile 99 = %f'%(ia.h2percentile(h,99),np.percentile(f,99)))


# In[3]:

if testing:
    f = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    h = ia.histogram(f)
    p = [1, 10, 50, 90, 99]
    print('percentiles:', p)
    print('h2percentile', ia.h2percentile(h,np.array(p)))
    print('np.percentile', np.percentile(f,p))


# ### Image Example

# In[4]:

if testing:
    import matplotlib.image as mpimg
    f = mpimg.imread('../data/cameraman.tif')  
    h = ia.histogram(f)
    p = [1, 10, 50, 90, 99]
    print('percentiles:', p)
    print('h2percentile', ia.h2percentile(h,np.array(p)))
    print('np.percentile', np.percentile(f,p))
    print('median', np.median(f))


# ## See also
# 
# - `ia636:iahistogram iahistogram`
# - `ia636:iapercentile` - Computes the percentile from the image
# 
# ## References
# 
# - `http://docs.scipy.org/doc/scipy/reference/stats.html SciPy Stats`
# - `http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.percentile.html numpy percentile`
# 
# ## Contributions
# 
# - Mariana Bento, August 2013

# In[ ]:




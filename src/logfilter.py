
# coding: utf-8

# # Function logfilter

# ## Synopse
# 
# Laplacian of Gaussian filter.
# 
# - **g = logfilter(f, sigma)**
# 
#   - **g**: Image.
# 
#   - **f**: Image. input image
#   - **sigma**: Double. scaling factor

# ## Description
# 
# Filters the image f by the Laplacian of Gaussian (LoG) filter with parameter sigma. This filter is also known as the Marr-Hildreth filter. Obs: to better efficiency, this implementation computes the filter in the frequency domain.

# In[1]:

import numpy as np
def logfilter(f, sigma):
    import ea979.src as ia
    
    f = np.array(f)

    if len(f.shape) == 1: f = f[newaxis,:]
    x = (np.array(f.shape)//2).astype(int)
    
    h = ia.log(f.shape, (np.array(f.shape)//2).astype(int), sigma)
    h = ia.dftshift(h)
    H = np.fft.fft2(h)
    if not ia.isccsym(H):
        raise ValueError('log filter is not symmetrical')        
    G = np.fft.fft2(f) * H
    g = np.fft.ifft2(G).real
    
    return g


# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python logfilter.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[3]:

if testing:
    get_ipython().magic('matplotlib inline')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    f = mpimg.imread('../data/cameraman.tif')

    g07 = ia.logfilter(f, 0.7)

    nb = ia.nbshow(3)
    nb.nbshow(f, 'Imagem original')
    nb.nbshow(ia.normalize(g07), 'LoG filter')
    nb.nbshow(g07 > 0, 'positive values')
    nb.nbshow()


# ### Example 2

# In[4]:

if testing:
    g5 = ia.logfilter(f, 5)
    g10 = ia.logfilter(f, 10)

    nb = ia.nbshow(2,2)
    nb.nbshow(ia.normalize(g5), 'sigma=5')
    nb.nbshow(g5 > 0, 'positive, sigma=5')
    nb.nbshow(ia.normalize(g10), 'sigma=10')
    nb.nbshow(g10 > 0, 'positive, sigma=10')
    nb.nbshow()


# In[ ]:




# In[ ]:




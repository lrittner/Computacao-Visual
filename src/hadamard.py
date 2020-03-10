
# coding: utf-8

# # Function hadamard
# 
# ## Synopse
# Hadamard Transform.
# 
#    - **F = iahadamard(f)**
#       - Output:
#           - **F**: Image.
#       - Input:
#           - **f**: Image.

# ## Function code

# In[1]:

import numpy as np

def hadamard(f):
    import ea979.src as ia
    f = np.asarray(f).astype(np.float64)
    if len(f.shape) == 1: f = f[:, newaxis]
    (m, n) = f.shape
    A = ia.hadamardmatrix(m)
    if (n == 1):
        F = np.dot(A, f)
    else:
        B = ia.hadamardmatrix(n)
        F = np.dot(np.dot(A, f), np.transpose(B))
    return F


# ## Examples
# 
# ### Example 1

# In[2]:

testing = (__name__ == "__main__")

if testing:
    get_ipython().system(' jupyter nbconvert --to python hadamard.ipynb')
    import numpy as np
    import sys,os
    import matplotlib.image as mpimg
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# In[3]:

if testing:
    f = mpimg.imread('../data/cameraman.tif')
    F = ia.hadamard(f)
    nb = ia.nbshow(2)
    nb.nbshow(f)
    nb.nbshow(ia.normalize(np.log(abs(F)+1)))
    nb.nbshow()


# ## Measuring time:

# In[ ]:

if testing:
    f = mpimg.imread('../data/cameraman.tif')
    print('Computational time is:')
    get_ipython().magic('timeit ia.hadamard(f)')


# In[ ]:




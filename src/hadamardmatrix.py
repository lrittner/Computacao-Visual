
# coding: utf-8

# # Function hadamardmatrix

# ## Synopse
# Kernel matrix for the Hadamard Transform.
# 
#    - **A = hadamardmatrix(N)**
#        - Output:
#            - **A**: Image.
#        - Input:
#            - **N**: Double.

# ## Function code

# In[5]:

import numpy as np
 
def hadamardmatrix(N):
 
    def bitsum(x):
        s = 0 * x
        while x.any():
            s += x & 1
            x >>= 1
        return s
 
    n = np.floor(np.log(N)/np.log(2))
 
    if 2**n != N:
        raise Exception('error: size {0} is not multiple of power of 2'.format(N))
 
    u, x = np.meshgrid(range(N), range(N))
 
    A = ((-1)**(bitsum(x & u)))/np.sqrt(N)
    return A


# In[1]:

testing = (__name__ == "__main__")

if testing:
    get_ipython().system(' jupyter nbconvert --to python hadamardmatrix.ipynb')
    import numpy as np
    import sys,os
    import matplotlib.image as mpimg
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ## Examples
# 
# ### Example 1

# In[2]:

if testing:
    A = ia.hadamardmatrix(128)
    ia.adshow(ia.normalize(A, [0, 255]))


# ### Example 2

# In[4]:

if testing:
    A = ia.hadamardmatrix(4)
    print(A)
    print(np.dot(A, np.transpose(A)))


# ## Measuring time:

# In[5]:

if testing:
    print('Computational time is:')
    get_ipython().magic('timeit ia.hadamardmatrix(128)')


# In[ ]:




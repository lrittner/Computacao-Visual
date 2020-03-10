
# coding: utf-8

# # Function dctmatrix
# 
# ## Synopse
# 
# Compute the Kernel matrix for the DCT Transform.
# 
# - **A = dctmatrix(N)**
# 
#   - **A**:output: DCT matrix NxN. 
#   - **N**:input: matrix size (NxN). 

# In[1]:

import numpy as np

def dctmatrix(N):
    x = np.resize(range(N), (len(range(N)), len(range(N)))) #matrix with columns index
    u = np.transpose(np.resize(range(N), (len(range(N)), len(range(N))))) #matrix with rows index
    alpha = np.ones((N,N)) * np.sqrt(2./N) # 1/sqrt(2/N)
    alpha[0,:] = np.sqrt(1./N) # alpha(u,x)
    A = alpha * np.cos((2*x+1)*u*np.pi / (2.*N)) # Cn(u,x)
    return A


# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python dctmatrix.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[3]:

if testing:
    np.set_printoptions(suppress=True, precision=4)
    A = ia.dctmatrix(4)
    print('Visualiza matriz DCT 4x4:\n',A)
    B = np.dot(A,np.transpose(A))
    
    print("\nVisualiza propriedade A*A'= I:\n", B)


# ### Example 2

# In[2]:

if testing:
    get_ipython().magic('matplotlib inline')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia
    A = ia.dctmatrix(128)
    ia.adshow(ia.normalize(A,[0,255]),'DCT 128x128')


# In[ ]:




# In[ ]:




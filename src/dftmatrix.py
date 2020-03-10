
# coding: utf-8

# # Function dftmatrix
# 
# ## Synopse
# 
# Kernel matrix for the 1-D Discrete Fourier Transform DFT.
# 
# - **A = dftmatrix(N)**
# 
#   - **A**: Output image, square N x N, complex
# 
# 
#   - **N**: Integer, number of points of the DFT

# In[1]:

import numpy as np

def dftmatrix(N):
    x = np.arange(N).reshape(N,1)
    u = x
    Wn = np.exp(-1j*2*np.pi/N)
    A = (1./np.sqrt(N)) * (Wn ** u.dot(x.T))
    return A


# ## Examples

# In[1]:

testing = (__name__ == "__main__")

if testing:
    get_ipython().system(' jupyter nbconvert --to python dftmatrix.ipynb')
    import numpy as np
    import sys,os
    import matplotlib.image as mpimg
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[2]:

if testing:
    A = ia.dftmatrix(128)
    ia.adshow(ia.normalize(A.real),'A.real')
    ia.adshow(ia.normalize(A.imag),'A.imag')


# Example 2
# ---------

# In[3]:

if testing:
    A = ia.dftmatrix(4)
    print('A=\n', A.round(1))
    print('A-A.T=\n', A - A.T)
    print((np.abs(np.linalg.inv(A)-np.conjugate(A))).max() < 10E-15)


# ### Example 3
# 
# Showing the product $\mathbf{x}\mathbf{u}^T$:

# In[4]:

if testing:
    u = x = np.arange(10).reshape(10,1)
    print('u xT=\n', u.dot(x.T))


# ## Equation
# 
# 
# $$ \begin{matrix}
#     W_N &=& \exp{\frac{-j2\pi}{N}} \\ A_N &=& \frac{1}{\sqrt{N}} (W_N)^{\mathbf{u} \mathbf{x}^T} \\ \mathbf{u} &=& \mathbf{x} = [0, 1, 2, \ldots, N-1]^T 
# \end{matrix} $$

# $$ \begin{matrix}
#         A_N       &=& A_N^T \ \mbox{symmetric} \\
#        (A_N)^{-1} &=& (A_N)^*\ \mbox{column orthogonality, unitary matrix}
# \end{matrix} $$

# ## See Also
# 
# - `dft` - Discrete Fourier Transform
# - `dftmatrixexamples` - Visualization of the DFT matrix
# 
# ## References
# 
# - http://en.wikipedia.org/wiki/DFT_matrix

# In[6]:

if testing:    
    print('testing dftmatrix')
    print(repr(np.floor(0.5 + 10E4*ia.dftmatrix(4).real) / 10E4) == repr(np.array(
          [[ 0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0. , -0.5,  0. ],
           [ 0.5, -0.5,  0.5, -0.5],
           [ 0.5,  0. , -0.5,  0. ]])))
    print(repr(np.floor(0.5 + 10E4*ia.dftmatrix(4).imag) / 10E4) == repr(np.array(
          [[ 0. ,  0. ,  0. ,  0. ],
           [ 0. , -0.5,  0. ,  0.5],
           [ 0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0.5,  0. , -0.5]])))


# In[ ]:




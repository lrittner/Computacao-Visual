#!/usr/bin/env python
# coding: utf-8

# # Function idft
# 
# ## Synopse
# 
# Inverse Discrete Fourier Transform.
# 
# - **f = iaidft(F)**
# 
#   - **f**: Image. 
# 
# 
#   - **F**: Image. 

# In[4]:


import numpy as np
import dftmatrix
def idft(F):
    s = F.shape
    if F.ndim == 1: F = F[np.newaxis,np.newaxis,:] 
    if F.ndim == 2: F = F[np.newaxis,:,:] 

    (p,m,n) = F.shape
    A = dftmatrix(m)
    B = dftmatrix(n)
    C = dftmatrix(p)
    Faux = np.conjugate(A).dot(F)
    Faux = Faux.dot(np.conjugate(B))
    f = np.conjugate(C).dot(Faux)/(np.sqrt(p)*np.sqrt(m)*np.sqrt(n))

    return f.reshape(s)


# ## Examples

# In[5]:


testing = (__name__ == "__main__")

if testing:
    get_ipython().system(' jupyter nbconvert --to python idft.ipynb')
    import numpy as np
    import sys,os
    import matplotlib.image as mpimg
    import dft, idft


# ### Example 1

# In[6]:


if testing:
    f = np.arange(24).reshape(4,6)
    F = dft.dft(f)
    g = idft.idft(F)
    print(np.round(g.real))


# In[ ]:


if False: #testing:
    import matplotlib.image as mpimg
    import circle, normalize, isdftsym
    
    f = mpimg.imread('../data/cameraman.tif')
    F = dft.dft(f)
    print(F.shape)
    H = circle.circle(F.shape, 50,[F.shape[0]/2,F.shape[1]/2] )
    H = normalize.normalize(H,[0,1])
    FH = F * idftshift.idftshift(H)
    print(isdftsym.isdftsym(FH))
    g= idft.idft(FH)
    plt.imshow(f)
    plt.imshow(dftview(F))
    plt.imshow(normalize(H,[0,255]))
    plt.imshow(dftview(FH))
    plt.imshow(normalize(abs(g)))


# ## Equation
# 
# $$ \begin{matrix}
#     f(x) &=& \frac{1}{N}\sum_{u=0}^{N-1}F(u)\exp(j2\pi\frac{ux}{N}) \\ & & 0 \leq x < N, 0 \leq u < N \\ \mathbf{f}          &=& \frac{1}{\sqrt{N}}(A_N)^* \mathbf{F} 
# \end{matrix} $$

# $$ \begin{matrix}
# f(x,y) &=& \frac{1}{NM}\sum_{u=0}^{N-1}\sum_{v=0}^{M-1}F(u,v)\exp(j2\pi(\frac{ux}{N} + \frac{vy}{M})) \\ & & (0,0) \leq (x,y) < (N,M), (0,0) \leq (u,v) < (N,M) \\ 
#     \mathbf{f} &=& \frac{1}{\sqrt{NM}} (A_N)^* \mathbf{F} (A_M)^*
# \end{matrix} $$    

# ## See also
# 
# - `iadft iadft`
# - `iadftview iadftview`
# - `iafftshift iafftshift`
# - `iaisdftsym iaisdftsym`
# 
# ## Contribution
# 

# In[ ]:






# coding: utf-8

# # Function comb
# 
# ## Synopse
# 
# Create a grid of impulses image.
# 
# - **g = comb(shape, delta, offset)**
# 
#   - **g**: Image. 
# 
# 
#   - **shape**: Image. output image dimensions (1-D, 2-D or 3-D).
#   - **delta**: Image. interval between the impulses in each dimension (1-D, 2-D or 3-D).
#   - **offset**: Image. offset in each dimension (1-D, 2-D or 3-D).

# In[1]:

import numpy as np
def comb(shape, delta, offset):

    shape = np.array(shape)
    assert shape.size <= 3
    g = np.zeros(shape) 
    if shape.size == 1:
        g[offset::delta] = 1
    elif shape.size == 2:
        g[offset[0]::delta[0], offset[1]::delta[1]] = 1
    elif shape.size == 3:
        g[offset[0]::delta[0], offset[1]::delta[1], offset[2]::delta[2]] = 1
    return g


# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python comb.ipynb')
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
    u1 = ia.comb(10, 3, 2)
    print('u1=',u1)
    u2 = ia.comb((10,), 3, 2)
    print('u2=',u2)


# ### Example 2

# In[3]:

if testing:
    u3 = ia.comb((7,9), (1,2), (0,1))
    print('u3=\n',u3)


# ### Example 3

# In[4]:

if testing:
    u4 = ia.comb((4,5,9), (2,1,2), (1,0,1))
    print(u4)


# ## Equation
# 
# One dimension:
# 
# $$ \begin{matrix} u(x)=\sum _{i=0}^{\infty}\delta \left( x-\left( ki+o\right) \right)\\
#     x\in [0,S_0-1]
#     \end{matrix}
#     $$

# $$\begin{matrix}
#     where\quad \delta (i)=\left\{ \begin{array}{ll}
#     1, & i=0\\
#     0, & otherwise
#     \end{array}\right.
#     \end{matrix}
#     $$

# N-dimension:
# 
# $$
# \begin{matrix}
# u\left( x_{0},x_{1},\cdots ,x_{N-1}\right) =\sum _{i_{0}=0}^{\infty}\sum _{i_{1}=0}^{\infty}\cdots \sum _{i_{N-1}=0}^{\infty}\delta \left( x_{0}-\left( k_{0}i_{0}+o_{0}\right) ,x_{1}-\left( k_{1}i_{1}+o_{1}\right) ,\cdots ,x_{N-1}-\left(k_{N-1}i_{N-1}+o_{N-1}\right) \right)\\
#     \left( x_{0},x_{1},\cdots ,x_{N-1}\right) \in \left[ \left( 0,0,\cdots ,0\right) ,\left( S_{0}-1,S_{1}-1,\cdots ,S_{N-1}-1\right) \right]
#     \end{matrix} $$

# $$\begin{matrix}
#     where\quad \delta (i_0,i_1,\ldots,i_{N-1})=\left\{ \begin{array}{ll}
#     1, & i_0=i_1=i_2=\ldots=i_{N-1}=0\\
#     0, & otherwise
#     \end{array}\right.
#     \end{matrix}
#     $$

# In[5]:

if testing:
    print('testing comb')
    print(repr(ia.comb(10, 3, 2)) == repr(np.array(
           [0., 0., 1., 0., 0., 1., 0., 0., 1., 0.])))
    print(repr(ia.comb((7,9), (3,4), (3,2))) == repr(np.array(
          [[0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 1., 0., 0., 0., 1., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0., 0., 0., 0.],
           [0., 0., 1., 0., 0., 0., 1., 0., 0.]])))


# In[ ]:




# In[ ]:



